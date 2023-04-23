import open3d as o3d


def main(filename: str):
    mesh = o3d.io.read_triangle_mesh(filename)
    mesh.compute_vertex_normals()
    mesh.paint_uniform_color([10, 10, 10])

    o3d.visualization.draw_geometries([mesh])

    pcd = mesh.sample_points_uniformly(number_of_points=len(mesh.vertices) * 100)
    o3d.visualization.draw_geometries([pcd])

    with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
        mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=10)

    mesh = mesh.filter_smooth_simple(number_of_iterations=30)

    mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh])
    o3d.io.write_triangle_mesh(f"output/{filename.split(sep='/')[1]}", mesh)


if __name__ == "__main__":
    main("data/Cylinder.STL")
