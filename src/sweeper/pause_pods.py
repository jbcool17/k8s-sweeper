# import os

# from kubernetes import client, config, utils


# def check_for_priorityclass(name):
#     print(name)

#     return True


# def check_for_deployment(name):
#     print(name)

#     return True


# def create_priorityclass(name):
#     # Set priority class
#     if not check_for_priorityclass(name):
#         os.system(f"cat ../data/priorityclass-*")
#     else:
#         print("pc already exists")


# def create_pause_pods():
#     # Set pause pods
#     print("create pause pods")


# def patch_pause_pods():
#     # Patch pause pods
#     print("patch pause pods")


# def delete_pause_pods():
#     # Patch pause pods
#     pritn("delete pause pods")


# def setup():
#     create_priorityclass("default")
#     create_priorityclass("overprovisioning")
#     create_pause_pods()
