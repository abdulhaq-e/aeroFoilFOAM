#be-ism-allah-alrahman-alrahim

import numpy as np

def generate(dat1, dat2, scale=1, W=0.5, H=20, D=20, Nx=250, ND=150, NT=105, NW=1,
             ExpT=800, ExpD=100, ExpArc=50,j=6,p=0.3):
    c = 1 #chord length
    
    #mesh dimensions
    #scale = 1
    #H = 20
    #D = 20 #length of downstream section
    #W = 0.5
    
    #mesh resolution parameters
    #Ni = 400        # Number of interpolation points along the foil
    #Nx = 250             # Number of mesh cells along the foil
    #ND = 150             # Number of cells in the downstream direction
    #NT = 102             # Number of cells the transverse direction
    #NW = 1               # Number of cells in the y-direction (along the foil axis)
    
    #Expansion rates
    #ExpT = 800          #Expansion rate in transverse direction
    #ExpD = 100           #Expansion rate in the downstream direction
    #ExpArc = 50          # Expansion rate along the inlet arc
    
    #take the data
    data1 = np.genfromtxt(dat1) #upper bits
    data2 = np.genfromtxt(dat2) #lower //
    
    Xu = data1[:,0]
    Xl = data2[:,0]
    
    Yu = data1[:,1]
    Yl = data2[:,1]
    
    #getting the camber from points is a pain, just assume it is there somewhere
    #x/c = 0.3 seems good
    
    c_max_idx = np.size(Xu)/2 - j
    print np.size(Xu)/2
    print Xu[c_max_idx]
    #initialize vertices:
    vertices = np.zeros((12,3))
    
    vertices[0,:] = [-D, 0, W] #0
    vertices[1,:]  = [Xu[c_max_idx], H, W] #1
    vertices[2,:]  = [Xu[-1], H, W] #2
    vertices[3,:]  = [D, H, W] #3
    vertices[4,:]  = [0, 0, W] #4
    vertices[5,:]  = [Xu[c_max_idx], Yu[c_max_idx], W] #5
    vertices[6,:]  = [Xl[c_max_idx], Yl[c_max_idx], W] #6
    vertices[7,:]  = [Xu[-1], Yu[-1], W] #7
    vertices[8,:]  = [D, Yu[-1], W] #8
    vertices[9,:] = [Xl[c_max_idx], -H, W]
    vertices[10,:] = [Xu[-1],  -H, W]
    vertices[11,:] = [D, -H, W]
    
    #vertices_sym = vertices
    #vertices_sym[2] *= -1
    
    #this bit is making me dizzy, it's a Friday night...
    #Edge 4-5 and 16-17
    pts1 = np.array([ Xu[0:c_max_idx+1],  Yu[0:c_max_idx+1] , W*np.ones(np.size(Xu[0:c_max_idx+1])) ] )
    pts5 = np.array([ pts1[0,:], pts1[1,:], -pts1[2,:]])
    
    #Edge 5-7 and 17-19
    pts2 = np.array([ Xu[c_max_idx:], Yu[c_max_idx:], W*np.ones(np.size(Xu[c_max_idx:])) ]) 
    pts6 = np.array([ pts2[0,:], pts2[1,:], -pts2[2,:] ])
    
    #Edge 4-6 and 16-18
    pts3 = np.array([ Xl[0:c_max_idx+1], Yl[0:c_max_idx+1], W*np.ones(np.size(Xl[0:c_max_idx+1])) ])
    pts7 = np.array([ pts3[0,:], pts3[1,:], -pts3[2,:]])
    
    #Edge 6-7 and 18-19
    pts4 = np.array([ Xl[c_max_idx:],  Yl[c_max_idx:], W*np.ones(np.size(Xl[c_max_idx:])) ])
    pts8 = np.array([ pts4[0,:], pts4[1,:], -pts4[2,:] ])
    
    #Edge 0-1 and 12-13
    pts9 = np.array([ -H*np.cos(np.pi/4)+Xu[c_max_idx],  H*np.sin(np.pi/4), W])
    pts11 = np.array([ pts9[0], pts9[1], -pts9[2] ])
    
    #Edge 0-9 and 12-21
    pts10 = np.array([ -H*np.cos(np.pi/4)+Xu[c_max_idx], -H*np.sin(np.pi/4), W])
    pts12 = np.array([ pts10[0], pts10[1], -pts10[2] ])
    
    
    #Calculate number of mesh points along 4-5 and 4-6
    #Nleading = (c_max_idx/Ni)*Nx;
    #Nleading = Xu[c_max_idx]*Nx;
    Nleading = p*Nx
    # Calculate number of mesh points along 5-7 and 6-7
    Ntrailing = Nx-Nleading;
    
    #let's write this blockMeshDict:
    writeAerofoilDict(scale, vertices, Nleading, NT, NW, ND, Ntrailing, ExpArc, ExpT, ExpD,
                      pts1,pts2,pts3,pts4,pts5,pts6,pts7,pts8,pts9,pts10,pts11,pts12)
    
#def writeAerofoilDict(scale, vertices, Nleading, NT, NW, ND, Ntrailing, ExpArc, ExpT, ExpD,
#                      pts1,pts2,pts3,pts4,pts5,pts6,pts7,pts8,pts9,pts10,pts11,pts12):
#    fo = open('blockMeshDict', 'w')    
#    
#    #Write file
#    fo.write( '/*--------------------------------*- C++ -*----------------------------------*\\ \n')
#    fo.write( '| =========                 |                                                 | \n')
#    fo.write( '| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           | \n')
#    fo.write( '|  \\\\    /   O peration     | Version:  2.1.0                                 | \n')
#    fo.write( '|   \\\\  /    A nd           | Web:      www.OpenFOAM.com                      | \n')
#    fo.write( '|    \\\\/     M anipulation  |                                                 | \n')
#    fo.write( '\\*---------------------------------------------------------------------------*/ \n')
#    fo.write( 'FoamFile                                                                        \n')
#    fo.write( '{                                                                               \n')
#    fo.write( '    version     2.0;                                                            \n')
#    fo.write( '    format      ascii;                                                          \n')
#    fo.write( '    class       dictionary;                                                     \n')
#    fo.write( '    object      blockMeshDict;                                                 \n')
#    fo.write( '}                                                                               \n')
#    fo.write( '// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // \n')
#    fo.write( '\n')
#    fo.write( 'convertToMeters %f; \n' % (scale) )
#    fo.write( '\n')
#    fo.write( 'vertices \n')       
#    fo.write( '( \n')
#    for i in range(12):
#        fo.write( '    (%f %f %f)\n' % (vertices[i,0], vertices[i,1], vertices[i,2]))
#    for j in range(12):
#        fo.write( '    (%f %f %f)\n' % (vertices[j,0], vertices[j,1], -vertices[j,2]))
#    fo.write( '); \n')
#    fo.write( '\n')
#    fo.write( 'blocks \n')
#    fo.write( '( \n')
#    fo.write( '    hex (16 17 13 12 4 5 1 0)     (%i %i %i) edgeGrading (1 %f %f 1 %f %f %f %f 1 1 1 1) \n' % (Nleading, NT, NW,  1./ExpArc, 1./ExpArc, ExpT, ExpT, ExpT, ExpT))
#    fo.write( '    hex (17 19 14 13 5 7 2 1)     (%i %i %i) simpleGrading (1 %f 1) \n' % (Ntrailing, NT, NW,  ExpT))
#    fo.write( '    hex (19 20 15 14 7 8 3 2)     (%i %i %i) simpleGrading (%f %f 1) \n' % (ND, NT, NW,  ExpD, ExpT))
#    fo.write( '    hex (4 6 9 0 16 18 21 12)     (%i %i %i) edgeGrading (1 %f %f 1 %f %f %f %f 1 1 1 1) \n' % (Nleading, NT, NW, 1./ExpArc, 1./ExpArc, ExpT, ExpT, ExpT, ExpT))
#    fo.write( '    hex (6 7 10 9 18 19 22 21)    (%i %i %i) simpleGrading (1 %f 1) \n' % (Ntrailing, NT, NW,  ExpT))
#    fo.write( '    hex (7 8 11 10 19 20 23 22)   (%i %i %i) simpleGrading (%f %f 1) \n' % (ND, NT, NW,  ExpD, ExpT))
#    
#    fo.write( '); \n')
#    fo.write( '\n')
#    fo.write( 'edges \n')
#    fo.write( '( \n')
#    
#    fo.write( '    spline 4 5 \n')
#    fo.write( '        ( \n')
#    
#    for i in range(pts1.shape[1]):
#        fo.write( '            (%f %f %f) \n' % (pts1[0,i], pts1[1,i], pts1[2,i]))
#    fo.write( '        ) \n')
#    
#    fo.write( '    spline 5 7 \n')
#    fo.write( '        ( \n')
#    for i in range(pts2.shape[1]):
#        fo.write( '            (%f %f %f)\n' % (pts2[0,i], pts2[1,i], pts2[2,i]))
#    fo.write( '        ) \n')
#    
#    fo.write( '    spline 4 6 \n')
#    fo.write( '        ( \n')
#    for i in range(pts3.shape[1]):
#        fo.write( '            (%f %f %f)\n' % (pts3[0,i], pts3[1,i], pts3[2,i]))
#    fo.write( '        ) \n')
#    
#    fo.write( '    spline 6 7 \n')
#    fo.write( '        ( \n')
#    for i in range(pts4.shape[1]):
#        fo.write( '            (%f %f %f)\n' % (pts4[0,i], pts4[1,i], pts4[2,i]))
#    fo.write( '        ) \n')
#    
#    fo.write( '    spline 16 17 \n')
#    fo.write( '        ( \n')
#    for i in range(pts5.shape[1]):
#        fo.write( '            (%f %f %f)\n' % (pts5[0,i], pts5[1,i], pts5[2,i]))
#    fo.write( '        ) \n')
#    
#    fo.write( '    spline 17 19 \n')
#    fo.write( '        ( \n')
#    for i in range(pts6.shape[1]):
#        fo.write( '            (%f %f %f)\n' % (pts6[0,i], pts6[1,i], pts6[2,i]))
#    fo.write( '        ) \n')
#    
#    fo.write( '    spline 16 18 \n')
#    fo.write( '        ( \n')
#    for i in range(pts7.shape[1]):
#        fo.write( '            (%f %f %f)\n' % (pts7[0,i], pts7[1,i], pts7[2,i]))
#    fo.write( '        ) \n')
#    
#    fo.write( '    spline 18 19 \n')
#    fo.write( '        ( \n')
#    for i in range(pts8.shape[1]):
#        fo.write( '            (%f %f %f)\n' % (pts8[0,i], pts8[1,i], pts8[2,i]))
#    fo.write( '        ) \n')
#    
#    fo.write( '    arc 0 1 (%f %f %f) \n' %(pts9[0], pts9[1], pts9[2]))
#    fo.write( '    arc 0 9 (%f %f %f) \n' %(pts10[0], pts10[1] , pts10[2]))
#    fo.write( '    arc 12 13 (%f %f %f) \n' %(pts11[0], pts11[1] , pts11[2]))
#    fo.write( '    arc 12 21 (%f %f %f) \n' %(pts12[0], pts12[1] , pts12[2]))
#    
#    fo.write( '); \n')
#    fo.write( '\n')
#    fo.write( 'boundary \n')
#    fo.write( '( \n')
#    
#    fo.write( '    INLET \n')
#    fo.write( '    { \n')
#    fo.write( '        type patch; \n')
#    fo.write( '        faces \n')
#    fo.write( '        ( \n')
#    fo.write( '            (1 0 12 13) \n')
#    fo.write( '            (0 9 21 12) \n')
#    fo.write( '            (3 2 14 15) \n')
#    fo.write( '            (2 1 13 14) \n')
#    fo.write( '            (9 10 22 21) \n')
#    fo.write( '            (10 11 23 22) \n')
#    fo.write( '        ); \n')
#    fo.write( '    } \n')
#    fo.write( '\n')
#    
#    fo.write( '    OUTLET \n')
#    fo.write( '    { \n')
#    fo.write( '        type patch; \n')
#    fo.write( '        faces \n')
#    fo.write( '        ( \n')
#    fo.write( '            (11 8 20 23) \n')
#    fo.write( '            (8 3 15 20) \n')
#    fo.write( '        ); \n')
#    fo.write( '    } \n')
#    fo.write( '\n')
#    
#    fo.write( '    WALL \n')
#    fo.write( '    { \n')
#    fo.write( '        type wall; \n')
#    fo.write( '        faces \n')
#    fo.write( '        ( \n')
#    fo.write( '            (5 4 16 17) \n')
#    fo.write( '            (7 5 17 19) \n')
#    fo.write( '            (4 6 18 16) \n')
#    fo.write( '            (6 7 19 18) \n')
#    fo.write( '        ); \n')
#    fo.write( '    } \n')
#    fo.write( '    SYM \n')
#    fo.write( '    { \n')
#    fo.write( '        type empty; \n')
#    fo.write( '        faces \n')
#    fo.write( '        ( \n')
#    fo.write( '            (4 5 1 0) \n')
#    fo.write( '            (16 17 13 12) \n')
#    fo.write( '            (7 5 1 2) \n')
#    fo.write( '            (19 17 13 14) \n')
#    fo.write( '            (7 8 3 2) \n')
#    fo.write( '            (19 20 15 14) \n')
#    fo.write( '            (4 0 9 6) \n')
#    fo.write( '            (16 12 21 18) \n')
#    fo.write( '            (7 6 9 10) \n')
#    fo.write( '            (19 18 21 22) \n')
#    fo.write( '            (8 7 10 11) \n')
#    fo.write( '            (20 19 22 23) \n')
#    fo.write( '        ); \n')
#    fo.write( '    } \n')
#    fo.write( '); \n')
#    fo.write( ' \n')
#    fo.write( 'mergePatchPairs \n')
#    fo.write( '( \n')
#    fo.write( '); \n')
#    fo.write( ' \n')
#    fo.write( '// ************************************************************************* // \n')
#    
#    #Close file
#    fo.close()
    
    
def writeAerofoilDict(scale, vertices, Nleading, NT, NW, ND, Ntrailing, ExpArc, ExpT, ExpD,
                      pts1,pts2,pts3,pts4,pts5,pts6,pts7,pts8,pts9,pts10,pts11,pts12):
    fo = open('blockMeshDict', 'w')    
    
    #Write file
    fo.write( '/*--------------------------------*- C++ -*----------------------------------*\\ \n')
    fo.write( '| =========                 |                                                 | \n')
    fo.write( '| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           | \n')
    fo.write( '|  \\\\    /   O peration     | Version:  2.1.0                                 | \n')
    fo.write( '|   \\\\  /    A nd           | Web:      www.OpenFOAM.com                      | \n')
    fo.write( '|    \\\\/     M anipulation  |                                                 | \n')
    fo.write( '\\*---------------------------------------------------------------------------*/ \n')
    fo.write( 'FoamFile                                                                        \n')
    fo.write( '{                                                                               \n')
    fo.write( '    version     2.0;                                                            \n')
    fo.write( '    format      ascii;                                                          \n')
    fo.write( '    class       dictionary;                                                     \n')
    fo.write( '    object      blockMeshDict;                                                 \n')
    fo.write( '}                                                                               \n')
    fo.write( '// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // \n')
    fo.write( '\n')
    fo.write( 'convertToMeters %f; \n' % (scale) )
    fo.write( '\n')
    fo.write( 'vertices \n')       
    fo.write( '( \n')
    for i in range(12):
        fo.write( '    (%f %f %f)\n' % (vertices[i,0], vertices[i,1], vertices[i,2]))
    for j in range(12):
        fo.write( '    (%f %f %f)\n' % (vertices[j,0], vertices[j,1], -vertices[j,2]))
    fo.write( '); \n')
    fo.write( '\n')
    fo.write( 'blocks \n')
    fo.write( '( \n')
    fo.write( '    hex (4 5 17 16 0 1 13 12)     (%i %i %i) edgeGrading (1 1 %f %f 1 1 1 1 %f %f %f %f) \n' % (Nleading, NW, NT,   1./ExpArc, 1./ExpArc, ExpT, ExpT, ExpT, ExpT))
    fo.write( '    hex (5 7 19 17 1 2 14 13)     (%i %i %i) simpleGrading (1 1 %f) \n' % (Ntrailing, NW, NT,  ExpT))
    fo.write( '    hex (7 8 20 19 2 3 15 14)     (%i %i %i) simpleGrading (%f 1 %f) \n' % (ND, NW,  NT,  ExpD, ExpT))
    fo.write( '    hex (16 18 6 4 12 21 9 0)     (%i %i %i) edgeGrading (1 1 %f %f 1 1 1 1 %f %f %f %f) \n' % (Nleading, NW, NT,   1./ExpArc, 1./ExpArc, ExpT, ExpT, ExpT, ExpT))
    fo.write( '    hex (18 19 7 6 21 22 10 9)    (%i %i %i) simpleGrading (1 1 %f) \n' % (Ntrailing, NW,  NT, ExpT))
    fo.write( '    hex (19 20 8 7 22 23 11 10)   (%i %i %i) simpleGrading (%f 1 %f) \n' % (ND,  NW, NT,  ExpD, ExpT))
    
    fo.write( '); \n')
    fo.write( '\n')
    fo.write( 'edges \n')
    fo.write( '( \n')
    
    fo.write( '    spline 4 5 \n')
    fo.write( '        ( \n')
    
    for i in range(pts1.shape[1]):
        fo.write( '            (%f %f %f) \n' % (pts1[0,i], pts1[1,i], pts1[2,i]))
    fo.write( '        ) \n')
    
    fo.write( '    spline 5 7 \n')
    fo.write( '        ( \n')
    for i in range(pts2.shape[1]):
        fo.write( '            (%f %f %f)\n' % (pts2[0,i], pts2[1,i], pts2[2,i]))
    fo.write( '        ) \n')
    
    fo.write( '    spline 4 6 \n')
    fo.write( '        ( \n')
    for i in range(pts3.shape[1]):
        fo.write( '            (%f %f %f)\n' % (pts3[0,i], pts3[1,i], pts3[2,i]))
    fo.write( '        ) \n')
    
    fo.write( '    spline 6 7 \n')
    fo.write( '        ( \n')
    for i in range(pts4.shape[1]):
        fo.write( '            (%f %f %f)\n' % (pts4[0,i], pts4[1,i], pts4[2,i]))
    fo.write( '        ) \n')
    
    fo.write( '    spline 16 17 \n')
    fo.write( '        ( \n')
    for i in range(pts5.shape[1]):
        fo.write( '            (%f %f %f)\n' % (pts5[0,i], pts5[1,i], pts5[2,i]))
    fo.write( '        ) \n')
    
    fo.write( '    spline 17 19 \n')
    fo.write( '        ( \n')
    for i in range(pts6.shape[1]):
        fo.write( '            (%f %f %f)\n' % (pts6[0,i], pts6[1,i], pts6[2,i]))
    fo.write( '        ) \n')
    
    fo.write( '    spline 16 18 \n')
    fo.write( '        ( \n')
    for i in range(pts7.shape[1]):
        fo.write( '            (%f %f %f)\n' % (pts7[0,i], pts7[1,i], pts7[2,i]))
    fo.write( '        ) \n')
    
    fo.write( '    spline 18 19 \n')
    fo.write( '        ( \n')
    for i in range(pts8.shape[1]):
        fo.write( '            (%f %f %f)\n' % (pts8[0,i], pts8[1,i], pts8[2,i]))
    fo.write( '        ) \n')
    
    fo.write( '    arc 0 1 (%f %f %f) \n' %(pts9[0], pts9[1], pts9[2]))
    fo.write( '    arc 0 9 (%f %f %f) \n' %(pts10[0], pts10[1] , pts10[2]))
    fo.write( '    arc 12 13 (%f %f %f) \n' %(pts11[0], pts11[1] , pts11[2]))
    fo.write( '    arc 12 21 (%f %f %f) \n' %(pts12[0], pts12[1] , pts12[2]))
    
    fo.write( '); \n')
    fo.write( '\n')
    fo.write( 'boundary \n')
    fo.write( '( \n')
    
    fo.write( '    INLET \n')
    fo.write( '    { \n')
    fo.write( '        type patch; \n')
    fo.write( '        faces \n')
    fo.write( '        ( \n')
    fo.write( '            (1 13 12 0) \n')
    fo.write( '            (0 12 21 9) \n')
    fo.write( '        ); \n')
    fo.write( '    } \n')
    fo.write( '\n')
    
    fo.write( '    OUTLET \n')
    fo.write( '    { \n')
    fo.write( '        type patch; \n')
    fo.write( '        faces \n')
    fo.write( '        ( \n')
    fo.write( '            (8 11 23 20) \n')
    fo.write( '            (3 8 20 15) \n')
    fo.write( '        ); \n')
    fo.write( '    } \n')
    fo.write( '\n')
    
    fo.write( '    WALL \n')
    fo.write( '    { \n')
    fo.write( '        type wall; \n')
    fo.write( '        faces \n')
    fo.write( '        ( \n')
    fo.write( '            (4 5 17 16) \n')
    fo.write( '            (5 7 19 17) \n')
    fo.write( '            (4 6 18 16) \n')
    fo.write( '            (6 7 19 18) \n')
    fo.write( '        ); \n')
    fo.write( '    } \n')
    fo.write( '    topAndBottom \n')
    fo.write( '    { \n')
    fo.write( '        type patch; \n')
    fo.write( '        faces \n')
    fo.write( '        ( \n')
    fo.write( '            (3 15 14 2) \n')
    fo.write( '            (2 14 13 1) \n')
    fo.write( '            (9 21 22 10) \n')
    fo.write( '            (10 22 23 11) \n')
    fo.write( '        ); \n')
    fo.write( '    } \n')
    fo.write( '    SYM \n')
    fo.write( '    { \n')
    fo.write( '        type empty; \n')
    fo.write( '        faces \n')
    fo.write( '        ( \n')
    fo.write( '            (4 5 1 0) \n')
    fo.write( '            (12 13 17 16) \n')
    fo.write( '            (5 7 2 1) \n')
    fo.write( '            (13 14 19 17) \n')
    fo.write( '            (7 8 3 2) \n')
    fo.write( '            (14 15 20 19) \n')
    fo.write( '            (4 0 9 6) \n')
    fo.write( '            (18 21 12 16) \n')
    fo.write( '            (6 9 10 7) \n')
    fo.write( '            (19 22 21 18) \n')
    fo.write( '            (7 10 11 8) \n')
    fo.write( '            (20 23 22 19) \n')
    fo.write( '        ); \n')
    fo.write( '    } \n')
    fo.write( '); \n')
    fo.write( ' \n')
    fo.write( 'mergePatchPairs \n')
    fo.write( '( \n')
    fo.write( '); \n')
    fo.write( ' \n')
    fo.write( '// ************************************************************************* // \n')
    
    #Close file
    fo.close()
