import json
import os.path


def configuration_setting(setting_path, real_path=False, key='setting', find_node_handler=None):
    def __decorator_wrapper__(func):
        def __wrapper__(*args, **kwargs):
            if key not in kwargs.keys():
                if real_path:
                    json_path = setting_path
                else:
                    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    json_path = os.path.join(base_dir, setting_path)

                setting_result = None

                if os.path.exists(json_path):
                    with open(json_path, 'r') as json_file:
                        json_setting = json.load(json_file)
                        setting_result = json_setting

                if find_node_handler is not None and setting_result is not None:
                    setting_result = find_node_handler(setting_result)

                kwargs[key] = setting_result
            return func(*args, **kwargs)
        return __wrapper__
    return __decorator_wrapper__
