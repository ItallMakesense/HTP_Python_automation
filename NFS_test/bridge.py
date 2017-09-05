from fabric.api import env, output, put, sudo
import os.path

import constants as cs


env.password = cs.SERVER_HOST_PASSWORD
env.host_string = '@'.join((cs.SERVER_HOST_NAME, cs.SERVER_ADDRESS))
env.warn_only = True

output['everything'] = False

const = os.path.basename(cs.__file__)

def prepare(path, script_file):
    script_file_path = script_file.__file__
    script_file_name = os.path.basename(script_file_path)
    result = sudo('mkdir %s' % path)
    put(cs.__file__, path, use_sudo=True)
    put(script_file_path, path, use_sudo=True)
    return script_file_name

# def back_down(path, script_file):
#     script_file_path = script_file.__file__
#     script_file_name = os.path.basename(script_file.__file__)
#     sudo('rm {path}/{file} {path}/{const}'.format(
#          path=path, file=script_file_name, const=const))

def remote_shell(run_with, path, script_file, *args):
    script_file_name = prepare(path, script_file)
    result = sudo("{prog} {path}/{file} {args}".format(
        prog=run_with, path=path, file=script_file_name, args=' '.join(args)))
    return result

# result = sudo(f'mkdir {cs.SERVER_TEST_DIR}')
# print(result)
# result = put(cs.__file__, cs.SERVER_TEST_DIR, use_sudo=True)
# print(result.succeeded)
