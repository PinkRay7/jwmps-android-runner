import random
import psutil
import time
import threading
import tracemalloc
import sys
from typing import Dict, Any, Optional
from pathlib import Path
from os.path import dirname, realpath
import subprocess
import shlex
import os
import signal
import pandas as pd
import sys
from EventManager.Models.RunnerEvents import RunnerEvents
from EventManager.EventSubscriptionController import EventSubscriptionController
from ConfigValidator.Config.Models.RunTableModel import RunTableModel
from ConfigValidator.Config.Models.FactorModel import FactorModel
from ConfigValidator.Config.Models.RunnerContext import RunnerContext
from ConfigValidator.Config.Models.OperationType import OperationType
from ExtendedTyping.Typing import SupportsStr
from ProgressManager.Output.OutputProcedure import OutputProcedure as output

# Add the current script directory to the system path
current_dir = Path(__file__).parent.resolve()
sys.path.insert(0, str(current_dir))

# Import all functions from functions.py
from functions import (
    fibonacci, fibonacci_memo,
    knapsack, knapsack_memo,
    coin_change, coin_change_memo,
    levenshtein_distance, levenshtein_distance_memo,
    factorial, factorial_memo,
    matrix_chain_order, matrix_chain_order_memo,
    can_i_win, can_i_win_non_memo,
    can_partition_k_subsets, can_partition_k_subsets_memo,
    all_possible_fbt, all_possible_fbt_memo,
)
def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

class RunnerConfig:
    ROOT_DIR = Path(dirname(realpath(__file__)))

    # ================================ USER SPECIFIC CONFIG ================================
    """The name of the experiment."""
    name:                       str             = "function_performance_experiment"

    """The path in which Experiment Runner will create a folder with the name `self.name`, in order to store the
    results from this experiment."""
    results_output_path:        Path            = ROOT_DIR / 'experiments'

    """Experiment operation type."""
    operation_type:             OperationType   = OperationType.AUTO

    """The time Experiment Runner will wait after a run completes."""
    time_between_runs_in_ms:    int             = 1000

    def __init__(self):
        """Executes immediately after program start, on config load"""

        EventSubscriptionController.subscribe_to_multiple_events([
            (RunnerEvents.BEFORE_EXPERIMENT, self.before_experiment),
            (RunnerEvents.BEFORE_RUN       , self.before_run       ),
            (RunnerEvents.START_RUN        , self.start_run        ),
            (RunnerEvents.START_MEASUREMENT, self.start_measurement),
            (RunnerEvents.INTERACT         , self.interact         ),
            (RunnerEvents.STOP_MEASUREMENT , self.stop_measurement ),
            (RunnerEvents.STOP_RUN         , self.stop_run         ),
            (RunnerEvents.POPULATE_RUN_DATA, self.populate_run_data),
            (RunnerEvents.AFTER_EXPERIMENT , self.after_experiment )
        ])
        self.run_table_model = None  # Initialized later

        output.console_log("Custom config loaded")

        # Define the list of test cases
        # All args have a dummy first input since those runs seem to break
        self.test_cases = [
            {
                'name': 'Fibonacci',
                'func_normal': fibonacci,
                'func_memo': fibonacci_memo,
                'args': (
                    (1,),
                    (20,),
                    (40,)
                    # (50,)
                )
            },
            {
                'name': 'Knapsack',
                'func_normal': knapsack,
                'func_memo': knapsack_memo,
                'args': ((1, (1, 1), (1, 1), 2), #dummy
                         (5,(20,30,40), (2,3,4), 3),
                         (100, [random.randint(1, 50) for _ in range(20)], [random.randint(1, 10) for _ in range(20)], 20),
                         (300, [random.randint(5, 300) for _ in range(60)], [random.randint(3, 30) for _ in range(60)], 60)),
            },
            {
                'name': 'Coin Change',
                'func_normal': coin_change,
                'func_memo': coin_change_memo,
                'args': (((1, 2), 1), #dummy
                         ((1,3,4,5), 23),
                         ((1,2,5,10), 37),
                         ([random.randint(1, 20) for _ in range(15)], 120)
                        )
            },
            {
                'name': 'Levenshtein Distance',
                'func_normal': levenshtein_distance,
                'func_memo': levenshtein_distance_memo,
                'args': (("a", "a"), #dummy
                         ("kitten", "sitting"),
                         ("flawlessly", "lawfulness"),
                         ("intentionallocation", "executionlocarion")
                         ),
            },
            {
                'name': 'Factorial',
                'func_normal': factorial,
                'func_memo': factorial_memo,
                'args': ((1,), #dummy
                         (50,), 
                         (500,), 
                         (1000,)
                         )
            },
            {
                'name': 'Matrix Chain Multiplication',
                'func_normal': matrix_chain_order,
                'func_memo': matrix_chain_order_memo,
                'args': ((1, 1, (1,)), #dummy
                         (1, 4, (10, 20, 30, 40, 30)),
                         (1, 9, (5, 10, 20, 35, 50, 25, 40, 30, 25, 60)),
                         (1, 14, [random.randint(10, 75) for _ in range(15)])
                         ),
            },
            {
                'name': 'Can I Win',
                'func_normal': can_i_win, #TODO: same functions
                'func_memo': can_i_win_non_memo,  
                'args': ((1, 1), #dummy,
                         (25, 40),
                         (27, 50),
                         (35, 55),
                )
    
            },
            {
                'name': 'K-equal Sum Partitions',
                'func_normal': can_partition_k_subsets,# same functions
                'func_memo': can_partition_k_subsets_memo,  
                'args': (([1,1], 1), #dummy
                         ([5]*20, 4),
                         ([20]*1_000, 10),
                         ([15]*5_000, 15),
                )
            },
            {
                'name': 'All Possible Full Binary Trees',
                'func_normal': all_possible_fbt,
                'func_memo': all_possible_fbt_memo,
                'args': ((1,), #dummy
                         (15,),
                         (25,),
                         (35,)
                         )
            },
        ]


    def create_run_table_model(self) -> RunTableModel:
        """Create and return the run_table model here."""
        factor_function = FactorModel("function_name", [test_case['name'] for test_case in self.test_cases])
        factor_version = FactorModel("version", ["normal", "memoized"])
        
        # Define the run table model
        self.run_table_model = RunTableModel(
            factors=[factor_function, factor_version],
            exclude_variations=[],
            #repetitions = 5, uncomment this when we run the real experiment
            data_columns=[
                'cpu_time',
                'memory_usage',
                'avg_cpu_time',
                'avg_memory_usage',
                'total_cpu_time',
                'total_memory_usage',
                'total_energy'
            ]
        )
        return self.run_table_model


    def before_experiment(self) -> None:
        output.console_log("Experiment is about to start.")
        sys.setrecursionlimit(100000000)

    def before_run(self) -> None:
        output.console_log("A new run is about to start.")

    def start_run(self, context: RunnerContext) -> None:
        output.console_log("Run is starting.")
        self.clear_caches()
        # Initialize memory tracking
        # tracemalloc.start()
        self.main_pid = os.getpid()

    def clear_caches(self):
        for test_case in self.test_cases:
            func = test_case['func_memo']
            if hasattr(func, 'cache'):
                func.cache.clear()

    # def start_measurement(self, context: RunnerContext) -> None:
    #     output.console_log("Measurement is starting.")
    #     self.start_time = time.process_time()
    def start_measurement(self, context: RunnerContext) -> None:
        output.console_log("Measurement is starting.")
        self.total_start_time = time.process_time()
        # tracemalloc.start()
        profiler_cmd = f'powerjoular -l -p {self.main_pid} -f {context.run_dir / f"powerjoular.csv"}'
        self.profiler = subprocess.Popen(shlex.split(profiler_cmd))
        if self.profiler.poll() is None:
            output.console_log("Process started successfully.")
        else:
            output.console_log(f"Process failed with return code: {self.profiler.returncode}")

    
    
    def interact(self, context: RunnerContext) -> None:
        output.console_log("Interacting with the function.")
        factors = context.run_variation
        function_name = factors['function_name']
        version = factors['version']
        test_case = next((case for case in self.test_cases if case['name'] == function_name), None)

        if not test_case:
            output.console_log(f"Test case for function {function_name} not found.")
            return
        
        func = test_case['func_normal'] if version == 'normal' else test_case['func_memo']
        args = test_case['args']

        self.call_times = []
        self.memory_usages = []
        # def get_memory_usage():
        #     process = psutil.Process(os.getpid())
        #     memory_info = process.memory_info().rss
        #     return memory_info
        i = 0
        for arg in args:
            self.clear_caches()
            # print(arg)
            tracemalloc.start()
            mem_before = process_memory()
            time.sleep(1)
            # mem_before = get_memory_usage()
            start_time = time.process_time()
            func(*arg)

            current, peak = tracemalloc.get_traced_memory()
            mem_after = process_memory()
            used_mem = mem_after - mem_before
            print("{}:consumed memory: {:,}".format(
            mem_before, mem_after, mem_after - mem_before))
            tracemalloc.stop()
            end_time = time.process_time()
            cpu_time = end_time - start_time
            memory_usage =  peak / 1024

            self.call_times.append(cpu_time)
            self.memory_usages.append(memory_usage)

            output.console_log(f"Call {i+1}: CPU Time = {cpu_time:.6f}s, Memory Usage = {memory_usage:.2f}KB")
            i+=1


    def stop_measurement(self, context: RunnerContext) -> None:
        output.console_log("Measurement is stopping.")
        self.total_end_time = time.process_time()
        self.total_cpu_time = self.total_end_time - self.total_start_time
        self.total_memory_usage = sum(self.memory_usages) #was peak /1024
        os.kill(self.profiler.pid, signal.SIGINT)
        self.profiler.wait()
        if self.profiler.poll() is None:
            output.console_log("Process alive")
        else:
            output.console_log(f"Process killed with return code: {self.profiler.returncode}")

    def stop_run(self, context: RunnerContext) -> None:
        output.console_log("Run is stopping.")
        output.console_log(f"Total CPU Time: {self.total_cpu_time:.6f}s, Total Memory Usage: {self.total_memory_usage:.2f}KB")
        avg_cpu_time = sum(self.call_times) / len(self.call_times)
        avg_memory_usage = sum(self.memory_usages) / len(self.memory_usages)
        output.console_log(f"Average CPU Time per Call: {avg_cpu_time:.6f}s, Average Memory Usage per Call: {avg_memory_usage:.2f}KB")


    def populate_run_data(self, context: RunnerContext) -> Optional[Dict[str, SupportsStr]]:
        output.console_log("Populating run data.")
        
        avg_cpu_time = sum(self.call_times) / len(self.call_times)
        avg_memory_usage = sum(self.memory_usages) / len(self.memory_usages)
        
        cpu_times_str = ';'.join(f"{t:.6f}" for t in self.call_times)
        memory_usages_str = ';'.join(f"{m:.2f}" for m in self.memory_usages)

        # powerjoular.csv - Power consumption of the whole system
        # powerjoular.csv-PID.csv - Power consumption of that specific process
        power_data_file = context.run_dir / f"powerjoular.csv-{self.main_pid}.csv"
        if not power_data_file.exists():
            output.console_log(f"Power data file {power_data_file} not found.")
            return None

        df = pd.read_csv(power_data_file)


        total_energy = df['CPU Power'].sum()

        return {
            'cpu_time': cpu_times_str,
            'memory_usage': memory_usages_str,
            'avg_cpu_time': f"{avg_cpu_time:.6f}",
            'avg_memory_usage': f"{avg_memory_usage:.2f}",
            'total_cpu_time': f"{self.total_cpu_time:.6f}",
            'total_memory_usage': f"{self.total_memory_usage:.2f}",
            'total_energy': f"{total_energy:.6f}",
        }

    def after_experiment(self) -> None:
        output.console_log("Experiment has finished.")

    # ================================ DO NOT ALTER BELOW THIS LINE ================================
    experiment_path:            Path             = None
