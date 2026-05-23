import Lake
open Lake DSL

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.13.0"

package TrinityLean

@[default_target]
lean_lib TrinityLean
