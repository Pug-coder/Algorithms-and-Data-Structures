import numpy as np
import open3d as o3d
from bpa import BPA
from bpa import Triangle
from vis import img_to_pcd

if __name__ == "__main__":

    print("Loading a ply point cloud")

    # For single photo
    rgbd_image = img_to_pcd("cat")
    camera_intrinsic = o3d.camera.PinholeCameraIntrinsic(
        o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault
    )
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
        rgbd_image, camera_intrinsic
    )

    # For series of image use o3d.io.read_point_cloud(file_path)
    # use sfm to create ply file before that
    # pcd = o3d.io.read_point_cloud('./res/Gustav.ply')
    # Flipping, the pointcloud will be upside down without it
    pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(
            radius=0.1, max_nn=30
        )
    )

    # Down sampling picture PC if need
    # voxel_pcd = pcd.voxel_down_sample(voxel_size=1e-6)
    # print(len(voxel_pcd.points))
    # b = BPA(voxel_pcd)

    print(len(pcd.points))
    b = BPA(pcd)
    print("making mesh")
    triangles = b.make_mesh()
    f = open("alg_res/cat.ply", "w")

    vertices = []
    v2index = {}
    index_counter = 0
    faces = []
    for t in triangles:
        out = []
        for vertex in t.vertices:
            v = tuple(vertex)
            if v2index.get(v):
                out.append(v2index[v])
            else:
                v2index[v] = index_counter
                index_counter += 1
                out.append(v2index[v])
                vertices.append(v)
        faces.append(out)

    f.write("ply\n")
    f.write("format ascii 1.0\n")
    f.write("element vertex " + str(len(vertices)) + "\n")
    f.write("property float32 x\n")
    f.write("property float32 y\n")
    f.write("property float32 z\n")
    f.write("element face " + str(len(faces)) + "\n")
    f.write("property list uint8 int32 vertex_indices\n")
    f.write("end_header\n")

    for v in vertices:
        f.write(str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + "\n")
    for face in faces:
        f.write(
            "3 "
            + str(face[0])
            + " "
            + str(face[1])
            + " "
            + str(face[2])
            + "\n"
        )
    f.close()
