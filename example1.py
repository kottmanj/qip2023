# Dependencies:
# pip install tequila-basic
# pip install pyscf
# optional but recommended:
# pip install qulacs
# psi4 can be used as alternative to pyscf
import tequila as tq
import numpy
pi = numpy.pi

# initialize molecule
geometry = "h 0.0 0.0 0.0\nh 0.0 0.0 2.0"
basis_set="sto-3g"
mol = tq.Molecule(geometry=geometry, basis_set=basis_set)
H = mol.make_hamiltonian()

# initialize quantum circuit that prepares the Hartree-Fock state
U = mol.prepare_reference()

# it's just a bunch of logical X gates
print(U)

# let's simulate it
wfn = tq.simulate(U)
print("HF qubit-wavefunction:", wfn)

# initialize an expectationvalue and compute its energy
E = tq.ExpectationValue(H=H, U=U)
hf_energy = tq.simulate(E)
print("HF Energy: {:+2.4f}".format(hf_energy))

# compute the same thing with pyscf
hf_energy2 = mol.compute_energy("hf")
print("HF Energy: {:+2.4f}".format(hf_energy2))

# initilize a UCC doubles excitation between orbital 0 and 1 (or spin orbitals 0,1 and 2,3)
U01 = mol.make_excitation_gate(indices=[(0,2),(1,3)],angle="a")

# combine the circuits
U = U + U01

# simulate the wavefunction (now we need to set the variable in the excitation gate)
wfn = tq.simulate(U, variables={"a":1.0})
print("ucc wavefunction with a=1.0")
print(wfn)

# energy (as before)
E = tq.ExpectationValue(H=H, U=U)
# gradient
dE = tq.grad(E, "a")

# compile abstract datatypes (translates to simulator, can be altered with backend=.... keyword)
fE = tq.compile(E)
fdE = tq.compile(dE)

# compute some points
for a in numpy.linspace(0.0,4.0*pi,10):
    energy = fE(variables={"a":a})
    gradient = fdE(variables={"a":a})
    print("point {:+2.5f} with energy {:+2.5f} and gradient {:2.5f}".format(a,energy,gradient))

# classical energies (not very spectacular with H2)
fci = mol.compute_energy("fci") # CCSD, MP2, HF

# do a minimization
result = tq.minimize(E)
opt_variables = result.variables
wfn = tq.simulate(U, variables=opt_variables)
print("opt ucc wavefunction:")
print(wfn)
print("UCC Energy: {:+2.4f}".format(result.energy))
print("FCI Energy: {:+2.4f}".format(fci))
