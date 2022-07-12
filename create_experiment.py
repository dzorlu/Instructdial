
import os
import json
from collections import defaultdict
from types import SimpleNamespace
from typing import List
from create_data_text2text import encode_tasks


from dataclasses import dataclass, field, asdict

@dataclass
class Config:
    task_files: List
    outputfile: str
    tasksfiles_folder: str
    configfile: str
    datasets_excluded: List = field(default_factory=[])
    no_instr: bool = False
    no_option: bool = False
    max_task_size: int = -1
    instruction_option_size: int = 400
    instruction_binary_size: int = 100
    cross_task_options_prob: int = 0
    none_of_above_prob: float = 0.
    noshuffle: bool = False
    max_data: int = -1
    max_task_size: int = -1
    configfile: str = 'config.json'



train_task_file_path = 'tasks_files/tasks_files_full_train'
train_task_files = os.listdir(train_task_file_path)

test_task_file_path = 'tasks_files/tasks_files_full_test'
test_task_files= os.listdir(test_task_file_path)

train_config_file = 'configs/config_tasks2.json'
train_config = json.load(open(train_config_file, 'r'))

# create dataset to task mapping
dataset_to_task_mapping = defaultdict(list)
for task_name, v in train_config.items():
    if 'datasets' not in v:
        continue
    for dt in v.get('datasets'):
        dataset_to_task_mapping[dt].append(task_name)

    


for test_task_file in train_task_files:
    print("*"*100)
    
    leave_one_out_train_task = set(train_task_files) - set([test_task_file])
    test_task = test_task_file.split('.')[0]
    print(f"generating training / test data for {test_task}")
    
    leave_one_out_train_task = [t.split('.')[0] for t in leave_one_out_train_task]

    # remove tasks that are associated with datasets for the test task.
    test_datasets = train_config.get(test_task, {}).get('datasets',[])
    print(f"test datasets that wil be removed: {test_datasets} from training set.")
    
    if not test_datasets:
        raise ValueError(f"cannot found the datasets associated with {test_task}")
    tasks_to_remove = list()
    for test_dataset in test_datasets:
        to_remove = dataset_to_task_mapping.get(test_dataset)
        tasks_to_remove.extend(to_remove)


    # # create config - train
    config = Config(
        task_files=list(leave_one_out_train_task),
        datasets_excluded=test_datasets,
        outputfile=f'train_{test_task}.json',
        tasksfiles_folder='tasks_files/tasks_files_full_train/',
        configfile='config.json'
    )
    config = asdict(config)
    config['task-files'] = config['task_files']

    with open('config.json','w') as f:
        json.dump(config, f)

    config = SimpleNamespace(**config)
    encode_tasks(config)

    # create config - test

    config = Config(
        task_files=[test_task],
        datasets_excluded=[],
        outputfile=f'test_{test_task}.json',
        tasksfiles_folder='tasks_files/tasks_files_full_test/',
        configfile='config.json'
    )
    config = asdict(config)
    config['task-files'] = config['task_files']

    with open('config.json','w') as f:
        json.dump(config, f)
    config = SimpleNamespace(**config)
    encode_tasks(config)






    

