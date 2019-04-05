class Quantum:
    def __init__(self):
        self.width = 0.0

    def schrodinger(basic_args, electron_potential):
    """
    return normalized hamiltonian with each eigen value (n = 1, 2, 3) and wave function in rectangler mesh

    Args
        - mesh : Rectangler Mesh (Dolfin Class)
        - potential : 2d electro static potential calculated in Poisson Equation 
        - device : Original Class of device structure
        - cons : Original Class of constant value

    Return
        - wavefunction_dict: Dict{"subband_number": [nx, nz], "subband_number": [nx, nz], ......}
    """
    # initialize some config value
    device = basic_args.device
    mesh = basic_args.device.mesh_2d
    simcon = basic_args.simcon
    doner = basic_args.device.doner.flatten()
    germanium = basic_args.material
    constant = basic_args.constant

    subbands = simcon.subband_number+1
    # reshape potential from 2d rectangle shape to 1d array
    #potential = np.array([i for i in potential])
    #potential = np.reshape(potential, (device.nz+1,device.nx+1))

    # Function space of rectangle mesh
    V = FunctionSpace(mesh, 'CG', 1)

    # plot with matplotlib instead of paraview
    n = V.dim()
    d = mesh.geometry().dim()

    # Excerpt of x-axis and y-axis
    dof_coordinates = V.tabulate_dof_coordinates()
    dof_coordinates.resize((n, d))
    dof_x = dof_coordinates[:, 0]
    dof_y = dof_coordinates[:, 1]

    # dimention of rectangle mesh
    N = device.nz 
    L = device.zfi
    x, dx = np.linspace(0, L, N), L / N

    z, dz = np.linspace(0, L, N+1), L / N
    wavefunction = np.zeros((device.nz+1, device.nx+1))
    eigenvalue = np.zeros((subbands, device.nx+1))

    wavefunction_dict = {}
    eigenvalue_dict = {}

    for subband in range(0, subbands):
        # calculate eigen vector and eigen value for each slice of rectangle mesh
        for index in range(device.nx + 1):
            #if(device.gate_ini < index*device.dx and index*device.dx < device.gate_fin):
            vector = electron_potential[:, index]
            H = makeHamiltonian(N, dx, vector, material=germanium, constant=constant)
            w, v = np.linalg.eigh(H)
            temp = v[:, subband]

            # eigen vector is alreadz normalized!!!
            wavefunction[:, index] = -1*temp
            eigenvalue[subband, index] = w[subband] / constant.Q

        wavefunction_dict[subband+1] = wavefunction
        eigenvalue_dict[subband+1] = eigenvalue[subband][:]

        """
        # reshape 2d wavefunction array to 1d array
        if("schrodinger" in device.flag):
            X = np.linspace(device.xin, device.xfi, device.nx+1)
            Y = np.linspace(device.yin, device.yfi, device.nz+1)
            X, Y = np.meshgrid(X, Y)

            # plot wavefunction
            fig = plt.figure()
            ax = fig.gca(projection="3d")
            ax.plot_surface(X, Y, wavefunction, linewidth=0.2, antialiased=True, cmap=plt.cm.coolwarm)
            ax.view_init(10, -120)
            plt.savefig("img/wave/wavefunction_" + str(iterate) + "-" + str(subband) + ".png")
        """

    print("Schrodinger Equation got finished!")

    return wavefunction_dict, eigenvalue_dict