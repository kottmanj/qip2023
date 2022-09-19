# dependencies
# madtequila installation will only work on linux-64 for now (sorry)
# pip install tequila-basic
# conda install madtequila -c kottmann
# pip install qulacs
import tequila as tq

# mol can be used in the same way as in the other examples
mol = tq.Molecule(geometry=geometry)
print(mol)

H = mol.make_hamiltonian()
U = mol.make_ansatz(name="SPA")
E = tq.ExpectationValue(H=H, U=U)

result = tq.minimize(E)


