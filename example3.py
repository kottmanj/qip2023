# dependencies
# pip install tequila-basic
# pip install pyscf
# pip install qulacs
import tequila as tq

# same as in example2 just with plain basis set
geometry = "Be 0.0 0.0 0.0\nH 0.0 0.0 1.5\nH 0.0 0.0 -1.5"
mol = tq.Molecule(geometry=geometry, basis_set="sto-3g")
print(mol)

H = mol.make_hamiltonian()
U = mol.make_ansatz(name="UpCCD") # automatic SPA construction not supported for basis_set implementation
E = tq.ExpectationValue(H=H, U=U)

result = tq.minimize(E)


