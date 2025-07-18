Creates binary FSTs from simple text format.

  Usage: fstcompile [text.fst [binary.fst]]

PROGRAM FLAGS:

  --acceptor: type = bool, default = false
  Input in acceptor format
  --arc_type: type = std::string, default = "standard"
  Output arc type
  --fst_type: type = std::string, default = "vector"
  Output FST type
  --isymbols: type = std::string, default = ""
  Input label symbol table
  --keep_isymbols: type = bool, default = false
  Store input label symbol table with FST
  --keep_osymbols: type = bool, default = false
  Store output label symbol table with FST
  --keep_state_numbering: type = bool, default = false
  Do not renumber input states
  --osymbols: type = std::string, default = ""
  Output label symbol table
  --ssymbols: type = std::string, default = ""
  State label symbol table

LIBRARY FLAGS:

Flags from: flags.cc
  --help: type = bool, default = false
  show usage information
  --helpshort: type = bool, default = false
  show brief usage information
  --tmpdir: type = std::string, default = "/tmp"
  temporary directory
  --v: type = int32_t, default = 0
  verbosity level

Flags from: fst.cc
  --fst_align: type = bool, default = false
  Write FST data aligned where appropriate
  --fst_default_cache_gc: type = bool, default = true
  Enable garbage collection of cache
  --fst_default_cache_gc_limit: type = int64_t, default = 1048576
  Cache byte size that triggers garbage collection
  --fst_read_mode: type = std::string, default = "read"
  Default file reading mode for mappable files
  --fst_verify_properties: type = bool, default = false
  Verify FST properties queried by TestProperties
  --save_relabel_ipairs: type = std::string, default = ""
  Save input relabel pairs to file
  --save_relabel_opairs: type = std::string, default = ""
  Save output relabel pairs to file

Flags from: symbol-table.cc
  --fst_compat_symbols: type = bool, default = true
  Require symbol tables to match when appropriate
  --fst_field_separator: type = std::string, default = "	 "
  Set of characters used as a separator between printed fields

Flags from: util.cc
  --fst_error_fatal: type = bool, default = true
  FST errors are fatal; o.w. return objects flagged as bad: e.g., FSTs: kError property set, FST weights: not a Member()

Flags from: weight.cc
  --fst_weight_parentheses: type = std::string, default = ""
  Characters enclosing the first weight of a printed composite weight (e.g., pair weight, tuple weight and derived classes) to ensure proper I/O of nested composite weights; must have size 0 (none) or 2 (open and close parenthesis)
  --fst_weight_separator: type = std::string, default = ","
  Character separator between printed composite weights; must be a single character

