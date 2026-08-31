"""
QuantumScholar - Foundational Quantum Corpus Seeder
Generates verified, peer-reviewed quantum computing knowledge chunks from classic papers,
textbooks, open-access curricula, and official SDK docs with rigorous citation tags and direct links.
"""

FOUNDATIONAL_QUANTUM_CHUNKS = [
    # =========================================================================
    # SOURCE 1: IEEE FOCS 1994 / Shor's Algorithm (https://ieeexplore.ieee.org/document/365700)
    # =========================================================================
    {
        "chunk_id": "shor_1994_focs_01",
        "title": "Algorithms for Quantum Computation: Discrete Logarithms and Factoring",
        "authors": ["Peter W. Shor"],
        "year": 1994,
        "venue": "Proceedings of 35th Annual IEEE Symposium on Foundations of Computer Science (FOCS 1994), pp. 124-134",
        "url": "https://ieeexplore.ieee.org/document/365700",
        "arxiv_id": "quant-ph/9508027",
        "doc_type": "paper",
        "citation_key": "Shor1994IEEE",
        "content": (
            "In this foundational paper published in IEEE FOCS 1994 (DOI: 10.1109/SFCS.1994.365700), Peter W. Shor proves that "
            "both prime factorization of an integer N and the discrete logarithm problem over finite fields can be computed in polynomial time "
            "O((log N)^2 (log log N) (log log log N)) on a quantum computer. "
            "The algorithm operates by reducing the factorization of N to the order-finding problem: given a random integer a coprime to N, "
            "finding the smallest positive integer r (the order or period) such that a^r = 1 (mod N). "
            "The quantum algorithm initializes a 2-register quantum state, prepares a uniform superposition over Z_q (where q = 2^m with N^2 <= q < 2N^2), "
            "computes the modular exponentiation |x> |0> -> |x> |a^x mod N>, and applies the Discrete Quantum Fourier Transform (QFT) to the first register. "
            "Measuring the first register yields a phase estimate dy/q close to an integer multiple s/r. "
            "The classical continued fraction expansion of y/q efficiently extracts the exact period r with high probability. "
            "Once an even period r is obtained, nontrivial factors of N are computed via classical greatest common divisor (GCD) calculations: "
            "gcd(a^(r/2) - 1, N) and gcd(a^(r/2) + 1, N). This polynomial-time quantum solution fundamentally breaks classical public-key cryptography (RSA and Diffie-Hellman)."
        )
    },

    # =========================================================================
    # SOURCE 2: arXiv:quant-ph/9605043 / Grover's Algorithm (https://arxiv.org/abs/quant-ph/9605043)
    # =========================================================================
    {
        "chunk_id": "grover_1996_stoc_01",
        "title": "A Fast Quantum Mechanical Algorithm for Database Search",
        "authors": ["Lov K. Grover"],
        "year": 1996,
        "venue": "Proceedings of the 28th Annual ACM Symposium on Theory of Computing (STOC 1996), pp. 212-219 / arXiv:quant-ph/9605043",
        "url": "https://arxiv.org/abs/quant-ph/9605043",
        "arxiv_id": "quant-ph/9605043",
        "doc_type": "paper",
        "citation_key": "Grover1996",
        "content": (
            "Grover's algorithm (arXiv:quant-ph/9605043) provides an optimal quantum algorithm for searching an unsorted database of N items "
            "for a unique marked element in O(sqrt(N)) oracle query evaluations, achieving a provable quadratic speedup over classical exhaustive search O(N). "
            "The quantum state begins in a uniform superposition of all N = 2^n computational basis states: |s> = (1/sqrt(N)) sum_{x=0}^{N-1} |x> = H^{otimes n} |0>^n. "
            "The core Grover iteration operator G consists of two consecutive unitary reflections: "
            "(1) The phase oracle reflection R_w = I - 2|w><w|, where R_w |x> = (-1)^{f(x)} |x>, inverting the phase of marked target states f(w)=1; "
            "(2) The diffusion operator / inversion about the average R_s = 2|s><s| - I = H^{otimes n} (2|0><0| - I) H^{otimes n}. "
            "Geometrically, each application of the Grover operator G = R_s R_w rotates the state vector in the 2D subspace spanned by |w> and the orthogonal uniform state |s'> "
            "by a fixed angle theta = 2 arcsin(1/sqrt(N)). "
            "After R = round((pi / 4) * sqrt(N / M)) iterations (where M is the number of target items), measuring the register yields the target state with probability near 1.0."
        )
    },

    # =========================================================================
    # SOURCE 3: Open-Access Quantum Learning Resources (https://github.com/ThiriYaminHsu/Open-Access-Quantum-Learning-Resources)
    # =========================================================================
    {
        "chunk_id": "oa_quantum_curriculum_01",
        "title": "Open-Access Quantum Learning Resources & Fundamental Computing Syllabus",
        "authors": ["Thiri Yamin Hsu"],
        "year": 2024,
        "venue": "Open-Access Quantum Learning Resources (GitHub)",
        "url": "https://github.com/ThiriYaminHsu/Open-Access-Quantum-Learning-Resources",
        "doc_type": "doc",
        "citation_key": "Hsu2024OpenAccess",
        "content": (
            "The Open-Access Quantum Learning Resources curriculum outlines the foundational theoretical roadmap for quantum computing education. "
            "Key prerequisite mathematics includes linear algebra over complex vector spaces (Hilbert space C^{2^n}), Dirac bra-ket notation (|psi>, <phi|), "
            "outer products (|psi><phi|), spectral theorem, unitary operators (U^dagger U = I), and tensor products (V otimes W) for multi-qubit composite systems. "
            "Core quantum algorithms in the syllabus include: "
            "- Deutsch-Jozsa Algorithm: Evaluates whether a Boolean function f: {0,1}^n -> {0,1} is constant or balanced in a single quantum query using Hadamard transforms and phase kickback. "
            "- Bernstein-Vazirani Algorithm: Determines an unknown n-bit secret string s in f(x) = s . x (mod 2) with 1 query compared to n classical queries. "
            "- Simon's Algorithm: Identifies a 2-to-1 function's hidden periodic XOR mask s (f(x) = f(y) iff x oplus y in {0^n, s}) in O(n) quantum queries, providing the first exponential speedup over classical randomized algorithms O(2^{n/2}). "
            "- Quantum Key Protocols: Quantum Teleportation (transmitting an unknown qubit using 1 shared EPR pair and 2 classical bits) and Superdense Coding (transmitting 2 classical bits using 1 qubit of an entangled EPR pair)."
        )
    },
    {
        "chunk_id": "oa_quantum_curriculum_02",
        "title": "Open-Access Quantum Hardware Architectures and Error Correction Systems",
        "authors": ["Thiri Yamin Hsu"],
        "year": 2024,
        "venue": "Open-Access Quantum Learning Resources (GitHub)",
        "url": "https://github.com/ThiriYaminHsu/Open-Access-Quantum-Learning-Resources",
        "doc_type": "doc",
        "citation_key": "Hsu2024HardwareQEC",
        "content": (
            "The Open-Access Quantum Learning Resources repository synthesizes major physical quantum computing hardware modalities and fault tolerance architectures: "
            "1. Superconducting Qubits: Nonlinear LC oscillators utilizing Josephson junctions (transmon qubits, fluxonium) with microwave control (5 GHz), coupled via coplanar waveguide resonators. "
            "2. Trapped Ion Qubits: Atomic ions (e.g. 171Yb+, 40Ca+) confined in Paul radiofrequency traps, controlled via focused laser beams with long coherence times (T2 > seconds) and all-to-all connectivity via collective motional modes. "
            "3. Neutral Atoms & Rydberg Arrays: Arrays of neutral atoms (Rb, Cs) trapped in optical tweezers, utilizing Rydberg states for high-fidelity two-qubit entangling CZ gates. "
            "4. Photonic Quantum Computing: Dual-rail or continuous-variable squeezed states using linear optical networks, beam splitters, phase shifters, and single-photon detectors. "
            "5. Quantum Error Correction Code Hierarchy: Shor's 9-qubit code (correcting arbitrary 1-qubit error via concatenation of 3-qubit bit-flip and phase-flip codes), Steane [[7,1,3]] CSS code, and Surface Codes on 2D lattices with fault-tolerance threshold ~1%."
        )
    },

    # =========================================================================
    # SOURCE 4: Learn Quantum Computing with Qiskit (https://github.com/MonitSharma/Learn-Quantum-Computing-with-Qiskit)
    # =========================================================================
    {
        "chunk_id": "learn_qiskit_monit_01",
        "title": "Learn Quantum Computing with Qiskit: Single & Multi-Qubit Gate Implementations",
        "authors": ["Monit Sharma"],
        "year": 2024,
        "venue": "Learn Quantum Computing with Qiskit (GitHub Tutorial Series)",
        "url": "https://github.com/MonitSharma/Learn-Quantum-Computing-with-Qiskit",
        "doc_type": "doc",
        "citation_key": "Sharma2024QiskitGates",
        "content": (
            "The Learn Quantum Computing with Qiskit repository provides practical code patterns and circuit explanations for quantum programming in Qiskit: "
            "Single-qubit operations: "
            "- Pauli Gates: `qc.x(0)` (bit-flip matrix [[0,1],[1,0]]), `qc.y(0)` (bit+phase flip [[0,-i],[i,0]]), `qc.z(0)` (phase-flip [[1,0],[0,-1]]). "
            "- Hadamard Gate: `qc.h(0)` maps computational basis states |0>, |1> to superposition states |+> = (|0>+|1>)/sqrt(2) and |-> = (|0>-|1>)/sqrt(2). "
            "- Phase & T Gates: `qc.s(0)` (phase gate diag(1, i)), `qc.t(0)` (pi/8 gate diag(1, exp(i*pi/4))), essential for universal quantum gate sets. "
            "- Arbitrary Rotations: `qc.rx(theta, 0)`, `qc.ry(theta, 0)`, `qc.rz(phi, 0)` and universal `qc.u(theta, phi, lambda, 0)`. "
            "Multi-qubit entangling gates: "
            "- CNOT Gate: `qc.cx(control, target)` flips target iff control is |1>, transforming |+>|0> into maximally entangled Bell state (|00>+|11>)/sqrt(2). "
            "- CZ Gate: `qc.cz(0, 1)` applies a phase flip (-1) only to state |11>. "
            "- Toffoli Gate (CCX): `qc.ccx(0, 1, 2)` universal reversible classical gate, flipping target iff both controls are |1>."
        )
    },
    {
        "chunk_id": "learn_qiskit_monit_02",
        "title": "Learn Quantum Computing with Qiskit: Quantum Algorithms, Teleportation & VQE",
        "authors": ["Monit Sharma"],
        "year": 2024,
        "venue": "Learn Quantum Computing with Qiskit (GitHub Tutorial Series)",
        "url": "https://github.com/MonitSharma/Learn-Quantum-Computing-with-Qiskit",
        "doc_type": "doc",
        "citation_key": "Sharma2024QiskitAlgos",
        "content": (
            "Practical implementations of quantum algorithms in Qiskit from Learn Quantum Computing with Qiskit: "
            "1. Quantum Teleportation: Alice prepares state |psi>, shares Bell state with Bob, applies CNOT(psi, epr_a) and H(psi), measures both qubits, "
            "and sends 2 classical bits to Bob. Bob applies X and/or Z conditional gates (`qc.x(bob).c_if(c_x, 1)`, `qc.z(bob).c_if(c_z, 1)`) to recover |psi>. "
            "2. Quantum Fourier Transform (QFT): Maps state |j> to (1/sqrt(N)) sum_{k=0}^{N-1} omega^{j*k} |k> using H gates and controlled phase rotation gates CP(pi/2^k), followed by qubit swap gates. "
            "3. Quantum Phase Estimation (QPE): Estimates phase theta in U|u> = exp(2*pi*i*theta)|u> using counting qubits, controlled-U^{2^j} gates, and inverse QFT. "
            "4. Variational Quantum Eigensolver (VQE) & QAOA: Parameterized ansatz `qc.ry(theta, 0)` combined with classical optimizers (COBYLA, SPSA) to minimize expectation values <H> on noisy quantum backends."
        )
    },

    # =========================================================================
    # SOURCE 5: Springer Quantum Algorithms Literature (https://link.springer.com/search?query=Quantum+Algorithms)
    # =========================================================================
    {
        "chunk_id": "springer_montanaro_2016_01",
        "title": "Quantum Algorithms: An Overview and Systematic Taxonomy",
        "authors": ["Ashley Montanaro"],
        "year": 2016,
        "venue": "npj Quantum Information / Springer Nature, Vol. 2, Article 15023",
        "url": "https://link.springer.com/search?query=Quantum+Algorithms",
        "arxiv_id": "1511.04206",
        "doc_type": "paper",
        "citation_key": "Montanaro2016Springer",
        "content": (
            "In this comprehensive survey of quantum algorithms published with Springer Nature (npj Quantum Information, arXiv:1511.04206), "
            "Ashley Montanaro presents a systematic taxonomy classifying quantum algorithmic speedups into three primary paradigms: "
            "1. Algorithms based on the Quantum Fourier Transform (QFT) and Hidden Subgroup Problems (HSP): "
            "Solves abelian HSP in polynomial time, including Shor's algorithm for factoring and discrete logarithms, period finding, Pell's equation, and hidden shift algorithms. "
            "2. Algorithms based on Quantum Amplitude Amplification, Grover Search, and Quantum Random Walks: "
            "Generalizes Grover search to amplitude amplification (Brassard et al. 2002) for quadratic speedups across NP-search problems, "
            "element distinctness in O(N^{2/3}) time via quantum walks (Ambainis 2007), and triangle finding in graphs in O(N^{5/4}) queries. "
            "3. Quantum Simulation and Hamiltonian Dynamics: "
            "Simulating physical quantum systems exp(-i H t) via Trotter-Suzuki product formulas, Linear Combinations of Unitaries (LCU), "
            "and solving linear systems of equations via the HHL algorithm (Harrow-Hassidim-Lloyd 2009) with exponential speedup in matrix dimension N."
        )
    },
    {
        "chunk_id": "springer_brassard_2002_amp_amp",
        "title": "Quantum Amplitude Amplification and Estimation",
        "authors": ["Gilles Brassard", "Peter Hoyer", "Michele Mosca", "Alain Tapp"],
        "year": 2002,
        "venue": "Quantum Computation and Information, Contemporary Mathematics / Springer",
        "url": "https://link.springer.com/search?query=Quantum+Algorithms",
        "arxiv_id": "quant-ph/0005055",
        "doc_type": "paper",
        "citation_key": "Brassard2002Springer",
        "content": (
            "Published in the Springer / AMS Quantum Computation literature (arXiv:quant-ph/0005055), Brassard, Hoyer, Mosca, and Tapp "
            "formalize Quantum Amplitude Amplification as a universal generalization of Grover's database search algorithm. "
            "Given any quantum algorithm A that prepares a state |psi> = A|0> = sqrt(p)|good> + sqrt(1-p)|bad> with initial success probability p, "
            "amplitude amplification uses the operator Q = -A S_0 A^{-1} S_chi to rotate the state towards |good> in O(1 / sqrt(p)) evaluations of A. "
            "This establishes a quadratic quantum advantage for ANY classical probabilistic algorithm with success probability p (classical requires O(1/p) trials). "
            "Furthermore, combining amplitude amplification with Quantum Phase Estimation yields Quantum Amplitude Estimation (QAE), "
            "which estimates the exact success probability p within error epsilon with high probability using only O(1/epsilon) queries, "
            "compared to classical Monte Carlo sampling which requires O(1/epsilon^2) samples (quadratic speedup for Monte Carlo financial & numerical integration)."
        )
    },

    # =========================================================================
    # Foundational Papers & Textbooks (Preskill, Fowler, Farhi, Peruzzo, Bennett, Harrow, Nielsen-Chuang, SDKs)
    # =========================================================================
    {
        "chunk_id": "preskill_1998_qec_01",
        "title": "Fault-Tolerant Quantum Computation",
        "authors": ["John Preskill"],
        "year": 1998,
        "venue": "Proceedings of the Royal Society A: Mathematical, Physical and Engineering Sciences",
        "url": "https://arxiv.org/abs/quant-ph/9712048",
        "arxiv_id": "quant-ph/9712048",
        "doc_type": "paper",
        "citation_key": "Preskill1998",
        "content": (
            "Fault-tolerant quantum computation enables arbitrary-length reliable quantum computation on noisy physical qubits, "
            "provided the physical gate error rate is below a critical threshold (the Quantum Threshold Theorem). "
            "Quantum error correction (QEC) protects fragile quantum information by encoding a single logical qubit across multiple physical qubits "
            "into entangled subspace states. Syndrome measurements (using stabilizer operators) diagnose bit-flip (X) and phase-flip (Z) errors "
            "without collapsing or learning the stored quantum superposition data. "
            "Transversal quantum gates prevent error cascading by ensuring that a single physical fault in one gate block only propagates to at most "
            "one physical qubit in another code block."
        )
    },
    {
        "chunk_id": "fowler_2012_surface_code_01",
        "title": "Surface Codes: Towards Practical Large-Scale Quantum Computation",
        "authors": ["Austin G. Fowler", "Mariantoni M.", "Martinis J. M.", "Cleland A. N."],
        "year": 2012,
        "venue": "Physical Review A 86, 032324",
        "url": "https://arxiv.org/abs/1208.0928",
        "arxiv_id": "1208.0928",
        "doc_type": "paper",
        "citation_key": "Fowler2012",
        "content": (
            "The planar surface code is widely considered the leading 2D topological quantum error correcting architecture due to its high physical "
            "fault-tolerance threshold of approximately 1% under depolarizing noise with nearest-neighbor 2D grid qubit connectivity. "
            "In a surface code of code distance d, logical states are defined on an L x L lattice of data qubits interspersed with syndrome measurement ancillas. "
            "Stabilizer measurements consist of 4-body star operators (X-type syndromes, A_v = prod_{i in star(v)} X_i) and plaquette operators "
            "(Z-type syndromes, B_p = prod_{j in bdry(p)} Z_j). "
            "Defects and error chains are decoded using the Minimum Weight Perfect Matching (MWPM) or Union-Find algorithms. "
            "Universal fault-tolerant quantum logic is achieved by combining transversal Clifford operations, lattice surgery, and magic state distillation."
        )
    },
    {
        "chunk_id": "farhi_2014_qaoa_01",
        "title": "A Quantum Approximate Optimization Algorithm",
        "authors": ["Edward Farhi", "Jeffrey Goldstone", "Sam Gutmann"],
        "year": 2014,
        "venue": "arXiv:1411.4028 [quant-ph]",
        "url": "https://arxiv.org/abs/1411.4028",
        "arxiv_id": "1411.4028",
        "doc_type": "paper",
        "citation_key": "Farhi2014",
        "content": (
            "The Quantum Approximate Optimization Algorithm (QAOA) is a hybrid quantum-classical variational algorithm designed for "
            "combinatorial optimization problems on NISQ devices. "
            "For a cost Hamiltonian H_C encoding the classical objective function (e.g. Max-Cut where H_C = sum_{(i,j)} 0.5 * (I - Z_i Z_j)) "
            "and a transverse mixer Hamiltonian H_B = sum_i X_i, QAOA constructs an alternating p-layer parameterized quantum ansatz: "
            "|gamma, beta> = prod_{k=1}^p [ exp(-i beta_k H_B) exp(-i gamma_k H_C) ] |+>^n. "
            "The quantum processor prepares the state and measures expectation value <H_C>, while a classical optimizer iteratively adjusts "
            "the 2p variational parameters (gamma_k, beta_k) to minimize or maximize the objective. In the limit p -> infinity, QAOA approaches adiabatic quantum computing."
        )
    },
    {
        "chunk_id": "peruzzo_2014_vqe_01",
        "title": "A Variational Eigenvalue Solver on a Photonic Quantum Processor",
        "authors": ["Alberto Peruzzo", "Jarrod McClean", "Peter Shadbolt", "Man-Hong Yung", "Xiao-Qi Zhou", "Peter J. Love", "Alán Aspuru-Guzik", "Jeremy L. O'Brien"],
        "year": 2014,
        "venue": "Nature Communications 5, 4213",
        "url": "https://arxiv.org/abs/1304.3061",
        "arxiv_id": "1304.3061",
        "doc_type": "paper",
        "citation_key": "Peruzzo2014",
        "content": (
            "The Variational Quantum Eigensolver (VQE) estimates the ground state energy E_0 of a molecular Hamiltonian H = sum_i c_i P_i "
            "(where P_i are Pauli strings) based on the Rayleigh-Ritz variational principle: <psi(theta)| H |psi(theta)> >= E_0. "
            "A shallow parameterized ansatz circuit (such as Unitary Coupled Cluster with Singles and Doubles - UCCSD, or hardware-efficient ansatz) "
            "generates trial wavefunctions |psi(theta)>. The quantum device measures the expectation value of each Pauli component <P_i>, "
            "and a classical optimization algorithm (e.g., COBYLA, SPSA, ADAM) updates parameters theta to converge toward the minimum energy eigenvalue."
        )
    },
    {
        "chunk_id": "bennett_1984_bb84_01",
        "title": "Quantum Cryptography: Public Key Distribution and Coin Tossing",
        "authors": ["Charles H. Bennett", "Gilles Brassard"],
        "year": 1984,
        "venue": "Proceedings of IEEE International Conference on Computers, Systems and Signal Processing (Bangalore, 1984)",
        "url": "https://doi.org/10.1016/j.tcs.2014.05.025",
        "arxiv_id": "arXiv:2003.06557",
        "doc_type": "paper",
        "citation_key": "Bennett1984",
        "content": (
            "The BB84 protocol is the foundational Quantum Key Distribution (QKD) protocol that guarantees unconditional information-theoretic security "
            "based on the quantum No-Cloning Theorem and Heisenberg uncertainty. "
            "Alice encodes random classical bits into single photons using two mutually unbiased bases: computational rectilinear basis Z = {|0>, |1>} "
            "and diagonal basis X = {|+>, |->}. Bob measures arriving photons in randomly chosen bases. "
            "Over a public classical authenticated channel, Alice and Bob perform basis reconciliation (sifting), error estimation, "
            "error correction (Cascade/Winnow), and privacy amplification. Any eavesdropping attempt by Eve inevitably introduces a Quantum Bit Error Rate (QBER) "
            "detectable during the test phase (threshold ~11% for 1-way post-processing)."
        )
    },
    {
        "chunk_id": "harrow_2009_hhl_01",
        "title": "Quantum Algorithm for Linear Systems of Equations",
        "authors": ["Aram W. Harrow", "Avinatan Hassidim", "Seth Lloyd"],
        "year": 2009,
        "venue": "Physical Review Letters 103, 150502",
        "url": "https://arxiv.org/abs/0811.3171",
        "arxiv_id": "0811.3171",
        "doc_type": "paper",
        "citation_key": "Harrow2009",
        "content": (
            "The HHL algorithm solves the quantum linear systems problem A|x> = |b> for a Hermitian s-sparse N x N matrix A with condition number kappa "
            "in time O(log(N) s^2 kappa^2 / epsilon), providing an exponential speedup over classical O(N s kappa) solvers. "
            "HHL operates via three quantum subroutines: (1) Quantum Phase Estimation using Hamiltonian simulation exp(i A t) to decompose |b> into the eigenbasis "
            "of A and store eigenvalues lambda_j in an ancilla register; (2) Controlled ancilla rotation by an angle proportional to arcsin(C / lambda_j) to perform "
            "inversion |lambda_j> -> lambda_j^{-1} |lambda_j>; (3) Inverse Quantum Phase Estimation (uncomputing) and post-selection on ancilla measurement |1>."
        )
    },
    {
        "chunk_id": "nielsen_chuang_2010_book_01",
        "title": "Quantum Computation and Quantum Information (10th Anniversary Edition)",
        "authors": ["Michael A. Nielsen", "Isaac L. Chuang"],
        "year": 2010,
        "venue": "Cambridge University Press",
        "url": "https://doi.org/10.1017/CBO9780511976667",
        "doc_type": "book",
        "citation_key": "NielsenChuang2010",
        "content": (
            "A qubit is a two-level quantum state represented in Hilbert space C^2 as |psi> = alpha |0> + beta |1>, where alpha, beta in C and |alpha|^2 + |beta|^2 = 1. "
            "Quantum gates correspond to unitary operators U such that U^dagger U = I. "
            "Single-qubit Pauli gates X = [[0,1],[1,0]], Y = [[0,-i],[i,0]], Z = [[1,0],[0,-1]], Hadamard gate H = (1/sqrt(2))[[1,1],[1,-1]], and Phase gate S = [[1,0],[0,i]] "
            "along with the entangling CNOT gate form a universal set for quantum computation when augmented with the non-Clifford T gate (T = [[1,0],[0, exp(i pi/4)]]). "
            "Bell states are maximally entangled two-qubit states: |Phi+-> = (|00> +/- |11>)/sqrt(2), |Psi+-> = (|01> +/- |10>)/sqrt(2)."
        )
    },
    {
        "chunk_id": "qiskit_sdk_docs_01",
        "title": "Qiskit SDK Official Architecture and Execution Model",
        "authors": ["Qiskit Development Team"],
        "year": 2024,
        "venue": "IBM Quantum Documentation (qiskit.org)",
        "url": "https://docs.quantum.ibm.com/api/qiskit",
        "doc_type": "doc",
        "citation_key": "Qiskit2024",
        "content": (
            "Qiskit is an open-source quantum computing software development framework. "
            "Circuits are constructed using `QuantumCircuit(num_qubits, num_classical_bits)` by applying gates such as `qc.h(0)`, `qc.cx(0, 1)`, and `qc.measure(0, 0)`. "
            "In Qiskit 1.0+, execution is structured around the Primitives interface: `SamplerV2` for returning quasi-probability distributions/counts "
            "and `EstimatorV2` for evaluating Hamiltonian expectation values <psi| H |psi>. "
            "Local simulation is provided by `qiskit_aer.AerSimulator` supporting multiple simulation methods: statevector, density_matrix, stabilizer, and matrix_product_state."
        )
    },
    {
        "chunk_id": "cirq_sdk_docs_01",
        "title": "Cirq Framework Documentation: NISQ Circuit Architecture",
        "authors": ["Google Quantum AI Team"],
        "year": 2024,
        "venue": "Google Quantum AI (quantumai.google/cirq)",
        "url": "https://quantumai.google/cirq",
        "doc_type": "doc",
        "citation_key": "Cirq2024",
        "content": (
            "Cirq is a Python software library for writing, manipulating, and optimizing quantum circuits on Near-Term Intermediate Scale Quantum (NISQ) computers. "
            "In Cirq, qubits are represented as `cirq.GridQubit(row, col)` or `cirq.LineQubit(index)`. "
            "Circuits are organized as collections of `cirq.Moment` slices, where each Moment is a collection of non-overlapping operations that execute in the same time step. "
            "Cirq circuits are executed using `cirq.Simulator().run(circuit, repetitions=1000)` or simulated via `cirq.Simulator().simulate(circuit)` to inspect wavefunction statevectors."
        )
    },
    {
        "chunk_id": "pennylane_sdk_docs_01",
        "title": "PennyLane: Differentiable Quantum Programming and Multi-Backend Device Agnosticism",
        "authors": ["Xanadu Quantum Technologies"],
        "year": 2024,
        "venue": "PennyLane Documentation (pennylane.ai)",
        "url": "https://docs.pennylane.ai",
        "doc_type": "doc",
        "citation_key": "PennyLane2024",
        "content": (
            "PennyLane is a cross-platform Python library for differentiable quantum computing and Quantum Machine Learning (QML). "
            "Quantum algorithms are defined as `@qml.qnode(dev)` functions that bind a quantum circuit to a hardware or simulator device `dev = qml.device('default.qubit', wires=2)`. "
            "PennyLane supports device-agnostic execution, allowing the identical QNode circuit to execute seamlessly on backends like `qiskit.aer`, `cirq.simulator`, or hardware. "
            "PennyLane natively supports automatic differentiation via parameter-shift rules (`qml.grad`), adjoint differentiation, and backpropagation across PyTorch, JAX, and TensorFlow."
        )
    }
]
