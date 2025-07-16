"""
FST Decoder
Written by Ye Kyaw Thu
Last Update: 11 July 2025

Usage:
    python ./fst_decoder.py ./config.yaml --show-id < ./closed_test.txt > closed_test.hyp
    python ./fst_decoder.py ./config.yaml --show-id < ./open_test.txt > open_test.hyp

Reference: https://www.phontron.com/kyfd/
"""

import os
import sys
import yaml
import argparse
import time
from typing import List, Dict, Any
import pywrapfst as fst
import pynini
import tempfile

class ConfigError(Exception):
    pass

class DecoderError(Exception):
    pass

class FSTModel:
    def __init__(self, config, symbol_tables=None):
        """Initialize the FST model with configuration"""
        self.config = config
        self.symbol_tables = symbol_tables or {}
        self.fst = None
        
    def load(self):
        """Load the FST with explicit symbol tables"""
        try:
            fst_file = self.config.get('file')
            if not fst_file:
                raise ConfigError("No FST file specified in config")
                
            if not os.path.exists(fst_file):
                raise ConfigError(f"FST file not found: {fst_file}")

            print(f"Attempting to load FST from: {fst_file}", file=sys.stderr)
            
            # Load FST first
            try:
                self.fst = pynini.Fst.read(fst_file)
            except Exception as e:
                raise ConfigError(f"Failed to read FST file {fst_file}: {str(e)}")
                
            if self.fst.start() == -1:
                raise ConfigError("Loaded FST has no start state")

            # Attach symbol tables if paths are provided
            input_sym_path = self.config.get('input_symbols')
            if input_sym_path:
                if not os.path.exists(input_sym_path):
                    print(f"Warning: Input symbol table not found: {input_sym_path}", file=sys.stderr)
                else:
                    input_sym = pynini.SymbolTable.read_text(input_sym_path)
                    self.fst.set_input_symbols(input_sym)

            output_sym_path = self.config.get('output_symbols')
            if output_sym_path:
                if not os.path.exists(output_sym_path):
                    print(f"Warning: Output symbol table not found: {output_sym_path}", file=sys.stderr)
                else:
                    output_sym = pynini.SymbolTable.read_text(output_sym_path)
                    self.fst.set_output_symbols(output_sym)
                
            print(f"Successfully loaded FST with {self.fst.num_states()} states", file=sys.stderr)
            print(f"Input symbols: {'yes' if self.fst.input_symbols() else 'no'}", file=sys.stderr)
            print(f"Output symbols: {'yes' if self.fst.output_symbols() else 'no'}", file=sys.stderr)
            
        except Exception as e:
            raise ConfigError(f"Error loading FST: {str(e)}")

    def verify(self):
        """Verify the loaded FST meets basic requirements"""
        if self.fst is None:
            raise ConfigError("FST not loaded")
        if self.fst.start() == -1:
            raise ConfigError("FST has no start state")
        if self.fst.num_states() == 0:
            raise ConfigError("FST has no states")
        return True

class DecoderConfig:
    def __init__(self, config_file: str = None, args: Dict = None):
        self.config = {
            'input_format': 'text',
            'output_format': 'text',
            'nbest': 1,
            'beam_width': 0,
            'trim_width': 0.0,
            'print_duplicates': False,
            'print_input': False,
            'print_all': False,
            'sample': False,
            'negative_probs': False,
            'weights': [1.0],
            'input_symbols': None,
            'output_symbols': None,
            'unknown_symbol': '<unk>',
            'terminal_symbol': '</s>',
            'show_id': False,
            'models': []
        }
        
        self.symbol_tables = {'input': None, 'output': None}
        self.unknown_id = -1
        self.terminal_id = -1
        
        if config_file:
            self.load(config_file)
        if args:
            self._apply_args(args)  # Changed from apply_args to _apply_args
    
    def load(self, config_file: str):
        try:
            with open(config_file, 'r') as f:
                config_data = yaml.safe_load(f) or {}
            
            for key, value in config_data.items():
                if key in self.config:
                    self.config[key] = value
            
            # Load symbol tables with verification
            if self.config['input_symbols']:
                self.symbol_tables['input'] = fst.SymbolTable.read_text(self.config['input_symbols'])
                if self.config['unknown_symbol']:
                    self.unknown_id = self.symbol_tables['input'].find(self.config['unknown_symbol'])
                if self.config['terminal_symbol']:
                    self.terminal_id = self.symbol_tables['input'].find(self.config['terminal_symbol'])
            
            if self.config['output_symbols']:
                self.symbol_tables['output'] = fst.SymbolTable.read_text(self.config['output_symbols'])
                
        except Exception as e:
            raise ConfigError(f"Config loading error: {str(e)}")
    
    def _apply_args(self, args: Dict):
        """Apply command-line arguments to configuration"""
        for key, value in args.items():
            if value is not None and key in self.config:
                # Handle special cases
                if key == 'weights':
                    self.config[key] = [float(w) for w in value.split(',')]
                elif key in ['nbest', 'beam_width']:
                    self.config[key] = int(value)
                elif key == 'trim_width':
                    self.config[key] = float(value)
                elif key in ['print_input', 'print_all', 'sample', 'negative_probs', 'print_duplicates']:
                    self.config[key] = bool(value)
                elif key == 'show_id':
                    self.config[key] = bool(value)
                else:
                    self.config[key] = value

class Decoder:
    def __init__(self, config: DecoderConfig):
        self.config = config
        self.sentence_id = 0
        self.multiplier = -1 if config.config['negative_probs'] else 1
        self.unknown_words = []
        
        # Initialize models with verification
        self.models = []

        for model_config in self.config.config['models']:
            try:
                print(f"\nInitializing model with config: {model_config}", file=sys.stderr)
                model = FSTModel(model_config, self.config.symbol_tables)
                print("Model object created, attempting to load...", file=sys.stderr)
                model.load()
                # In Decoder.__init__, after model.load():
                model.verify()
                if model.fst is None:
                    raise DecoderError(f"Model loaded but fst is None: {model_config.get('file', 'unknown')}")
                
                # Additional verification
                print(f"Model loaded successfully. Start state: {model.fst.start()}", file=sys.stderr)
                print(f"Num states: {model.fst.num_states()}", file=sys.stderr)
                print(f"Input symbols: {model.fst.input_symbols()}", file=sys.stderr)
                print(f"Output symbols: {model.fst.output_symbols()}", file=sys.stderr)
                
                self.models.append(model)
            except Exception as e:
                raise DecoderError(f"Model initialization failed: {str(e)}")

    def decode(self, input_stream, output_stream) -> bool:
        try:
            print("-- Starting FST Decoder --", file=sys.stderr)
            
            if self.config.config['input_format'] == 'text':
                return self._process_text(input_stream, output_stream)
            else:
                raise DecoderError("FST input format not yet implemented")
                
        except Exception as e:
            print(f"ERROR: {str(e)}", file=sys.stderr)
            return False
    
    def _process_text(self, input_stream, output_stream) -> bool:

        for lineno, line in enumerate(input_stream):
            tokens = line.strip().split()
            if not tokens:
                continue
                
            try:
                input_fst = self._make_input_fst(tokens)
                best_fst = self._find_best_paths(input_fst)
                
                if best_fst.start() == -1:
                    print("WARNING: no path found", file=sys.stderr)
                    continue
                
                self._print_result(best_fst, output_stream, lineno)
                self.sentence_id += 1
                
            except Exception as e:
                #print(f"ERROR processing sentence: {str(e)}", file=sys.stderr)
                if self.config.config['show_id']:
                    print(f"# Skipped line {lineno}: {tokens}", file=sys.stderr)

                continue
                
        return True
    
    def _make_input_fst(self, tokens: List[str]):
        """Create input FST using symbol table mapping"""
        try:
            # Create empty FST with symbol tables
            input_fst = pynini.Fst()
            input_sym = self.config.symbol_tables['input']
            input_fst.set_input_symbols(input_sym)
            input_fst.set_output_symbols(input_sym)
            
            start_state = input_fst.add_state()
            input_fst.set_start(start_state)
            current_state = start_state
            self.unknown_words = []
            
            for token in tokens:
                next_state = input_fst.add_state()
                label = input_sym.find(token)
                
                if label == -1:
                    if self.config.unknown_id == -1:
                        raise DecoderError(f"Unknown token '{token}'")
                    label = self.config.unknown_id
                    self.unknown_words.append(token)
                
                input_fst.add_arc(current_state, 
                                pynini.Arc(label, label, 0.0, next_state))
                current_state = next_state
            
            input_fst.set_final(current_state, 0.0)
            return input_fst
            
        except Exception as e:
            raise DecoderError(f"Input FST creation failed: {str(e)}")

    def _find_best_paths(self, input_fst):
        """Find best paths with symbol verification"""
        try:
            # Verify symbol tables
            if not input_fst.input_symbols():
                raise DecoderError("Input FST missing input symbols")
            if not self.models[0].fst.input_symbols():
                raise DecoderError("Model FST missing input symbols")
                
            # Check symbol table compatibility
            input_symtab = input_fst.input_symbols()
            model_symtab = self.models[0].fst.input_symbols()

            input_syms = set(input_symtab.find(i) for i in range(input_symtab.num_symbols()))
            model_syms = set(model_symtab.find(i) for i in range(model_symtab.num_symbols()))


            common_syms = input_syms & model_syms
            print(f"Common symbols: {len(common_syms)}", file=sys.stderr)
            
            search_fst = input_fst.copy()
            
            for model in self.models:
                print(f"Composing with model: {model.config['file']}", file=sys.stderr)
                
                # Perform composition
                composed = pynini.compose(search_fst, model.fst)
                if composed.start() == -1:
                    print("Composition failed - possible symbol mismatch", file=sys.stderr)
                    print(f"Input FST symbols: {input_fst.input_symbols()}", file=sys.stderr)
                    print(f"Model FST symbols: {model.fst.input_symbols()}", file=sys.stderr)
                    return composed
                    
                search_fst = composed
                
            return pynini.shortestpath(search_fst)
            
        except Exception as e:
            raise DecoderError(f"Path finding error: {str(e)}")

    def _print_result(self, result_fst, output_stream, lineno: int):
        """Print results with proper symbol table handling"""
        try:
            if result_fst.start() == -1:
                print("WARNING: no path found", file=sys.stderr)
                return
                
            # Convert to string using symbol tables
            output_str = ""
            state = result_fst.start()
            while state != -1:
                arcs = list(result_fst.arcs(state))
                if not arcs:
                    break
                    
                arc = arcs[0]  # Take first arc
                olabel = arc.olabel
                
                # Handle output symbols
                if self.config.symbol_tables['output']:
                    out_sym = self.config.symbol_tables['output'].find(olabel)

                    if out_sym == "<eps>" or out_sym == -1:
                        pass  # skip epsilon and undefined
                    else:
                        output_str += f"{out_sym} "
                else:
                    if olabel != 0:
                        output_str += f"{olabel} "


                state = arc.nextstate
            
            # Write output
            #line = f"{self.sentence_id}|||{output_str.strip()}"
            #print(line, file=output_stream)
            #print(output_str.strip(), file=output_stream)
            if self.config.config['show_id']:
                print(f"{lineno}|||{output_str.strip()}", file=output_stream)
            else:
                print(output_str.strip(), file=output_stream)

        except Exception as e:
            raise DecoderError(f"Output generation error: {str(e)}")

    def _get_input_symbol(self, label: int, unk_idx: int) -> str:
        if label == self.config.unknown_id:
            if unk_idx < len(self.unknown_words):
                return self.unknown_words[unk_idx]
            return "<unk>"
        return self.config.symbol_tables['input'].find(label) or str(label)
    
    def _get_output_symbol(self, label: int, unk_idx: int) -> str:
        if label == self.config.unknown_id:
            if unk_idx < len(self.unknown_words):
                return self.unknown_words[unk_idx]
            return "<unk>"
        return self.config.symbol_tables['output'].find(label) or str(label)

def parse_args():
    parser = argparse.ArgumentParser(description="KYFD - A WFST-based decoder")
    parser.add_argument("config", help="Configuration file (YAML format)")
    parser.add_argument("-i", "--input", choices=["text", "fst"], dest="input_format",
                       help="Input format (text or fst)")
    parser.add_argument("-o", "--output", choices=["text", "score", "component"], dest="output_format",
                       help="Output format")
    parser.add_argument("-n", "--nbest", type=int, help="Number of best paths to output")
    parser.add_argument("-w", "--weights", help="Comma-separated list of weights")
    parser.add_argument("-u", "--unknown", help="Unknown symbol")
    parser.add_argument("-t", "--terminal", help="Terminal symbol")
    parser.add_argument("--beam", type=int, dest="beam_width", help="Beam width")
    parser.add_argument("--trim", type=float, dest="trim_width", help="Trim threshold")
    parser.add_argument("--print-input", action="store_true", help="Print input sequence")
    parser.add_argument("--print-all", action="store_true", help="Print all arcs")
    parser.add_argument("--sample", action="store_true", help="Sample paths instead of shortest path")
    parser.add_argument("--negative", action="store_true", dest="negative_probs",
                       help="Treat weights as negative log probabilities")
    parser.add_argument("--show-id", action="store_true", help="Show original line number in output")

    
    return parser.parse_args()

def main():
    args = parse_args()
    
    try:
        config = DecoderConfig(args.config, vars(args))
        decoder = Decoder(config)
        success = decoder.decode(sys.stdin, sys.stdout)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"FATAL ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

