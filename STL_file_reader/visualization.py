import open3d as o3d

if __name__ == "__main__":
    mesh: o3d.geometry.TriangleMesh = o3d.io.read_triangle_mesh("output/Cylinder.STL")
    mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh])
