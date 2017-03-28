MODULE Adder;
CONST N := 0;
IN x, y: [N] BIT; ci: BIT;
OUT s: [N] BIT; co: BIT;
BEGIN
  S.0(X.0, Y.0, ci); (* inputs in cell 0*)
  FOR o:=1 N-1 DO
    S.i(X.i,Y.i,S[i-1].co) (* inputs in cell i *)
  END;
  FOR i 0..N-1 DO
    Z.i:=S.i.z
  END;
  co:=S.7.co
END Adder.
