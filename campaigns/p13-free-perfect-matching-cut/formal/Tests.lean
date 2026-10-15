import Challenge
open P13FreePerfectMatchingCut
example : sourceWitness ⟨3,[[0,1,2]]⟩ [true,false,false] = true := by native_decide
example : sourceWitness ⟨3,[[0,1,2]]⟩ [true,true,false] = false := by native_decide
example : perfectCut ⟨2,[(0,1)]⟩ [false,true] = true := by native_decide
