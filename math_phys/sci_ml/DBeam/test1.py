import numpy as np
import open3d as o3d
import trimesh
import pygmsh
import meshio


sphere = trimesh.creation.box(extents=(100, 60, 8))
sphere.vertices += 1e-2*np.random.randn(*sphere.vertices.shape)

geom = pygmsh.geo.Geometry()

with pygmsh.geo.Geometry() as geom:
    '''geom.add_polygon(
        [
            [0.0, 0.0],
            [1.0, -0.2],
            [1.1, 1.2],
            [0.1, 0.7],
        ],
        mesh_size=0.1,
    )'''
    geom.add_box(0, 100, 0, 60, 0, 8, mesh_size=2.0)
    msh = geom.generate_mesh()
cells = msh.get_cells_type('triangle')
meshed = meshio.Mesh(points=msh.points, cells={'triangle': cells})

# geom.synchronize()
# msh = geom.generate_mesh()
print(meshed.points.shape, meshed.cells[0].data.shape)

v = o3d.utility.Vector3dVector(meshed.points)
f = o3d.utility.Vector3iVector(meshed.cells[0].data)
# mesh = o3d.geometry.TriangleMesh(v, f)
pcd = o3d.geometry.PointCloud(v)
pcd.paint_uniform_color((0.6, 0.6, 0.6))
pcd.colors = o3d.utility.Vector3dVector([(0.5, 0.5, 0.5)]*10000)
# pcd.colors = o3d.utility.Vector3dVector(np.random.uniform(0, 1, size=(10000, 3)))
# mesh.vertex_colors = o3d.utility.Vector3dVector(np.random.uniform(0, 1, size=(10000, 3)))
# voxel_grid = o3d.geometry.VoxelGrid.create_from_triangle_mesh(mesh, voxel_size=0.2)
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=0.5)
o3d.visualization.draw_geometries([voxel_grid])
