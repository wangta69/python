from easydict import EasyDict
import json


class JsonConfigFileManager:
    """Json설정파일을 관리한다"""

    def __init__(self, file_path):
        self.values = EasyDict()
        if file_path:
            self.file_path = file_path  # 파일경로 저장
            self.reload()

    def reload(self):
        """설정을 리셋하고 설정파일을 다시 로딩한다"""
        self.clear()
        if self.file_path:
            with open(self.file_path, 'r') as f:
                self.values.update(json.load(f))

    def clear(self):
        """설정을 리셋한다"""
        self.values.clear()

    def update(self, in_dict):
        """기존 설정에 새로운 설정을 업데이트한다(최대 3레벨까지만)"""
        for (k1, v1) in in_dict.items():
            if isinstance(v1, dict):
                for (k2, v2) in v1.items():
                    if isinstance(v2, dict):
                        for (k3, v3) in v2.items():
                            self.values[k1][k2][k3] = v3
                    else:
                        self.values[k1][k2] = v2
            else:
                self.values[k1] = v1

    def export(self, save_file_name):
        """설정값을 json파일로 저장한다"""
        if save_file_name:
            with open(save_file_name, 'w') as f:
                json.dump(dict(self.values), f)


conf = JsonConfigFileManager('./config-manager.json')

# dict과 내용이 같다
print(conf.values)

# 대괄호[] 또는 점(.)을 이용하여 접근할 수 있다
print('epochs:', conf.values['epochs'])
print('epochs:', conf.values.epochs)

print('batch_size:', conf.values['model']['batch_size'])
print('batch_size:', conf.values.model.batch_size)

# 새로운 dict의 값으로 각 키별 업데이트한다 
conf.update({'epochs': 20, 'model': {'cells': 128}, 'patients': 3})

# 업데이트된 결과를 확인할 수 있다
print(conf.values)

# 현재 설정을 다른 파일명으로 내보낸다
conf.export('./config_new.json')