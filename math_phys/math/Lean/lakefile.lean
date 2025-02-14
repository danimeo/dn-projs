import Lake
open Lake DSL

package «p1» where
  -- add package configuration options here

lean_lib «P1» where
  -- add library configuration options here

@[default_target]
lean_exe «p1» where
  root := `Main
