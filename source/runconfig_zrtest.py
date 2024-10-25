import time
import tracemalloc
import sys
from typing import Dict, Any, Optional
from pathlib import Path
from os.path import dirname, realpath
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
    can_partition_k_subsets, can_partition_k_subsets_non_memo,
    all_possible_fbt, all_possible_fbt_memo,
)

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
        self.test_cases = [
            {
                'name': 'Fibonacci',
                'func_normal': fibonacci,
                'func_memo': fibonacci_memo,
                'args': (35,),  # modify as need
            },
            {
                'name': 'Knapsack',
                'func_normal': knapsack,
                'func_memo': knapsack_memo,
                'args': (50, 3, (10, 20, 30), (60, 100, 120)),
            },
            {
                'name': 'Coin Change',
                'func_normal': coin_change,
                'func_memo': coin_change_memo,
                'args': (3, 4, (1, 2, 3)),
            },
            {
                'name': 'Levenshtein Distance',
                'func_normal': levenshtein_distance,
                'func_memo': levenshtein_distance_memo,
                'args': ('kitten', 'sitting', 6, 7),
            },
            {
                'name': 'Factorial',
                'func_normal': factorial,
                'func_memo': factorial_memo,
                'args': (50,),
            },
            {
                'name': 'Matrix Chain Multiplication',
                'func_normal': matrix_chain_order,
                'func_memo': matrix_chain_order_memo,
                'args': (1, 4, (10, 20, 30, 40, 30)),
            },
            {
                'name': 'Can I Win',
                'func_normal': can_i_win_non_memo,
                'func_memo': can_i_win,  # This function already includes memoization
                'args': (10, 11),
            },
            {
                'name': 'K-equal Sum Partitions',
                'func_normal': can_partition_k_subsets_non_memo,
                'func_memo': can_partition_k_subsets,  # Already includes memoization
                'args': ([4, 3, 2, 3, 5, 2, 1], 4),
            },
            {
                'name': 'All Possible Full Binary Trees',
                'func_normal': all_possible_fbt,
                'func_memo': all_possible_fbt_memo,
                'args': (7,),
            },
        ]

    # def create_run_table_model(self) -> RunTableModel:
    #     """Create and return the run_table model here."""
    #     factor_function = FactorModel("function_name", [test_case['name'] for test_case in self.test_cases])
    #     factor_version = FactorModel("version", ["normal", "memoized"])
        
    #     # Define the run table model
    #     self.run_table_model = RunTableModel(
    #         factors=[factor_function, factor_version],
    #         exclude_variations=[],
    #         data_columns=['cpu_time', 'memory_usage']
    #     )
    #     return self.run_table_model
    def create_run_table_model(self) -> RunTableModel:
        """Create and return the run_table model here."""
        factor_function = FactorModel("function_name", [test_case['name'] for test_case in self.test_cases])
        factor_version = FactorModel("version", ["normal", "memoized"])
        
        # Define the run table model
        self.run_table_model = RunTableModel(
            factors=[factor_function, factor_version],
            exclude_variations=[],
            data_columns=[
                'cpu_time',
                'memory_usage',
                'avg_cpu_time',
                'avg_memory_usage',
                'total_cpu_time',
                'total_memory_usage'
            ]
        )
        return self.run_table_model

    def before_experiment(self) -> None:
        output.console_log("Experiment is about to start.")

    def before_run(self) -> None:
        output.console_log("A new run is about to start.")

    def start_run(self, context: RunnerContext) -> None:
        output.console_log("Run is starting.")
        self.clear_caches()
        # Initialize memory tracking
        tracemalloc.start()

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
        tracemalloc.start()
    # def interact(self, context: RunnerContext) -> None:
    #     output.console_log("Interacting with the function.")

    #     # Debug: Print attributes of RunnerContext and contents of run_variation
    #     # output.console_log(f"RunnerContext attributes: {dir(context)}")
    #     # output.console_log(f"run_variation type: {type(context.run_variation)}")
    #     # output.console_log(f"run_variation content: {context.run_variation}")

    #     # Get the current run parameters
    #     factors = context.run_variation  # Use run_variation directly as a factor dictionary
    #     function_name = factors['function_name']
    #     version = factors['version']

    #     # Find the corresponding test case based on function name
    #     test_case = next((case for case in self.test_cases if case['name'] == function_name), None)
    #     if not test_case:
    #         output.console_log(f"Test case for function {function_name} not found.")
    #         return

    #     # Call the function and record the result
    #     func = test_case['func_normal'] if version == 'normal' else test_case['func_memo']
    #     args = test_case['args']

    #     # Capture memory usage and function result
    #     result = func(*args)

    #     # Store the result for later use
    #     self.result = result
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
        num_calls = 5  

        for i in range(num_calls):
            self.clear_caches()
            start_time = time.process_time()
            tracemalloc.start()
            
            result = func(*args)

            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            end_time = time.process_time()
            
            cpu_time = end_time - start_time
            memory_usage = peak / 1024 

            self.call_times.append(cpu_time)
            self.memory_usages.append(memory_usage)

            output.console_log(f"Call {i+1}: CPU Time = {cpu_time:.6f}s, Memory Usage = {memory_usage:.2f}KB")


    # def stop_measurement(self, context: RunnerContext) -> None:
    #     output.console_log("Measurement is stopping.")
    #     self.end_time = time.process_time()
    #     self.cpu_time = self.end_time - self.start_time

    #     # Get memory usage
    #     current, peak = tracemalloc.get_traced_memory()
    #     tracemalloc.stop()
    #     self.memory_usage = peak / 1024  # Convert to KB
    def stop_measurement(self, context: RunnerContext) -> None:
        output.console_log("Measurement is stopping.")
        self.total_end_time = time.process_time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.total_cpu_time = self.total_end_time - self.total_start_time
        self.total_memory_usage = sum(self.memory_usages) #was peak /1024

    # def stop_run(self, context: RunnerContext) -> None:
    #     output.console_log("Run is stopping.")
    #     output.console_log(f"CPU Time: {self.cpu_time:.6f}s, Memory Usage: {self.memory_usage:.2f}KB")
    def stop_run(self, context: RunnerContext) -> None:
        output.console_log("Run is stopping.")
        output.console_log(f"Total CPU Time: {self.total_cpu_time:.6f}s, Total Memory Usage: {self.total_memory_usage:.2f}KB")
        avg_cpu_time = sum(self.call_times) / len(self.call_times)
        avg_memory_usage = sum(self.memory_usages) / len(self.memory_usages)
        output.console_log(f"Average CPU Time per Call: {avg_cpu_time:.6f}s, Average Memory Usage per Call: {avg_memory_usage:.2f}KB")


    # def populate_run_data(self, context: RunnerContext) -> Optional[Dict[str, SupportsStr]]:
    #     output.console_log("Populating run data.")
    #     return {
    #         'cpu_time': f"{self.cpu_time:.6f}",
    #         'memory_usage': f"{self.memory_usage:.2f}"
    #     }
    def populate_run_data(self, context: RunnerContext) -> Optional[Dict[str, SupportsStr]]:
        output.console_log("Populating run data.")
        
        avg_cpu_time = sum(self.call_times) / len(self.call_times)
        avg_memory_usage = sum(self.memory_usages) / len(self.memory_usages)
        
        cpu_times_str = ';'.join(f"{t:.6f}" for t in self.call_times)
        memory_usages_str = ';'.join(f"{m:.2f}" for m in self.memory_usages)
        
        return {
            'cpu_time': cpu_times_str,
            'memory_usage': memory_usages_str,
            'avg_cpu_time': f"{avg_cpu_time:.6f}",
            'avg_memory_usage': f"{avg_memory_usage:.2f}",
            'total_cpu_time': f"{self.total_cpu_time:.6f}",
            'total_memory_usage': f"{self.total_memory_usage:.2f}"
        }

    def after_experiment(self) -> None:
        output.console_log("Experiment has finished.")

    # ================================ DO NOT ALTER BELOW THIS LINE ================================
    experiment_path:            Path             = None
