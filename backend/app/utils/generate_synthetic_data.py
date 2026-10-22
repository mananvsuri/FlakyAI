"""Generate synthetic test execution data for development and testing."""

import argparse
import random
import csv
from datetime import datetime, timedelta
from pathlib import Path


def generate_synthetic_data(
    num_tests: int = 100,
    num_executions: int = 1000,
    flaky_ratio: float = 0.15,
    output_path: str = "../datasets/synthetic_test_data.csv"
):
    """Generate synthetic test execution dataset.
    
    Args:
        num_tests: Number of unique tests
        num_executions: Total number of executions
        flaky_ratio: Proportion of tests that are flaky
        output_path: Output CSV file path
    """
    random.seed(42)
    
    # Define test categories
    num_flaky = int(num_tests * flaky_ratio)
    num_stable_pass = int(num_tests * 0.50)
    num_stable_fail = int(num_tests * 0.30)
    num_insufficient = num_tests - num_flaky - num_stable_pass - num_stable_fail
    
    # Create test profiles
    tests = []
    test_id_counter = 1
    
    # Flaky tests (intermittent failures)
    for _ in range(num_flaky):
        tests.append({
            'test_id': f'test_{test_id_counter:04d}',
            'type': 'flaky',
            'base_pass_rate': random.uniform(0.3, 0.8),
            'duration_mean': random.uniform(0.5, 3.0),
            'duration_std': random.uniform(0.1, 0.5),
        })
        test_id_counter += 1
    
    # Stable passing tests
    for _ in range(num_stable_pass):
        tests.append({
            'test_id': f'test_{test_id_counter:04d}',
            'type': 'stable_pass',
            'base_pass_rate': 1.0,
            'duration_mean': random.uniform(0.3, 2.0),
            'duration_std': random.uniform(0.05, 0.2),
        })
        test_id_counter += 1
    
    # Stable failing tests
    for _ in range(num_stable_fail):
        tests.append({
            'test_id': f'test_{test_id_counter:04d}',
            'type': 'stable_fail',
            'base_pass_rate': 0.0,
            'duration_mean': random.uniform(0.5, 2.5),
            'duration_std': random.uniform(0.1, 0.3),
        })
        test_id_counter += 1
    
    # Insufficient data tests
    for _ in range(num_insufficient):
        tests.append({
            'test_id': f'test_{test_id_counter:04d}',
            'type': 'insufficient',
            'base_pass_rate': random.uniform(0.2, 0.9),
            'duration_mean': random.uniform(0.5, 2.0),
            'duration_std': random.uniform(0.1, 0.3),
        })
        test_id_counter += 1
    
    # Generate executions
    executions = []
    start_date = datetime(2024, 1, 1)
    
    projects = ['project_a', 'project_b', 'project_c']
    environments = ['staging', 'production', 'development']
    branches = ['main', 'develop', 'feature/auth', 'feature/checkout']
    
    execution_id = 1
    
    for _ in range(num_executions):
        test = random.choice(tests)
        
        # Determine number of executions for this test
        if test['type'] == 'insufficient':
            if random.random() < 0.7:  # Most insufficient tests have few executions
                continue
        
        # Generate timestamp
        days_offset = random.randint(0, 90)
        hours_offset = random.randint(0, 23)
        minutes_offset = random.randint(0, 59)
        timestamp = start_date + timedelta(days=days_offset, hours=hours_offset, minutes=minutes_offset)
        
        # Determine outcome
        if test['type'] == 'flaky':
            # Flaky tests have intermittent failures
            passes = random.random() < test['base_pass_rate']
            outcome = 'PASSED' if passes else 'FAILED'
        elif test['type'] == 'stable_pass':
            outcome = 'PASSED' if random.random() < 0.99 else 'FAILED'  # Occasional random failure
        elif test['type'] == 'stable_fail':
            outcome = 'FAILED' if random.random() < 0.95 else 'PASSED'  # Mostly fails
        else:
            outcome = 'PASSED' if random.random() < test['base_pass_rate'] else 'FAILED'
        
        # Generate duration
        duration = max(0.1, random.gauss(test['duration_mean'], test['duration_std']))
        if outcome == 'FAILED':
            duration *= random.uniform(1.0, 2.0)  # Failed tests often take longer
        
        # Retry count
        retry_count = 0
        if outcome == 'FAILED' and random.random() < 0.3:
            retry_count = random.randint(1, 3)
        
        # Error message
        error_message = ''
        if outcome == 'FAILED':
            errors = [
                'Timeout waiting for element',
                'Connection refused',
                'Assertion failed: expected true, got false',
                'NullPointerException',
                'Element not found',
                'Network timeout',
                'Database connection error',
            ]
            error_message = random.choice(errors)
        
        execution = {
            'test_id': test['test_id'],
            'execution_id': f'exec_{execution_id:06d}',
            'timestamp': timestamp.isoformat() + 'Z',
            'outcome': outcome,
            'duration': round(duration, 3),
            'retry_count': retry_count,
            'error_message': error_message,
            'project_id': random.choice(projects),
            'environment': random.choice(environments),
            'branch': random.choice(branches),
            'commit_hash': f'{random.randint(0, 0xFFFFFF):06x}',
            'changed_files': random.randint(1, 20),
            'runner_id': f'runner_{random.randint(1, 5)}',
            'is_flaky_label': 'FLAKY' if test['type'] == 'flaky' else 'NOT_FLAKY' if test['type'] in ['stable_pass', 'stable_fail'] else 'UNKNOWN',
            'label_source': 'synthetic',
        }
        
        executions.append(execution)
        execution_id += 1
    
    # Sort by timestamp
    executions.sort(key=lambda x: x['timestamp'])
    
    # Write to CSV
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    fieldnames = [
        'test_id', 'execution_id', 'timestamp', 'outcome', 'duration',
        'retry_count', 'error_message', 'project_id', 'environment',
        'branch', 'commit_hash', 'changed_files', 'runner_id',
        'is_flaky_label', 'label_source'
    ]
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(executions)
    
    print(f"✅ Generated {len(executions)} executions for {num_tests} tests")
    print(f"📁 Saved to: {output_file}")
    print(f"📊 Distribution:")
    print(f"   - Flaky tests: {num_flaky}")
    print(f"   - Stable passing: {num_stable_pass}")
    print(f"   - Stable failing: {num_stable_fail}")
    print(f"   - Insufficient data: {num_insufficient}")
    print(f"\n⚠️  This is SYNTHETIC DATA - clearly labeled throughout the application")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate synthetic test execution data')
    parser.add_argument('--num-tests', type=int, default=150, help='Number of unique tests')
    parser.add_argument('--num-executions', type=int, default=1500, help='Total executions')
    parser.add_argument('--flaky-ratio', type=float, default=0.15, help='Proportion of flaky tests')
    parser.add_argument('--output', type=str, default='../datasets/synthetic_test_data.csv', help='Output path')
    
    args = parser.parse_args()
    generate_synthetic_data(args.num_tests, args.num_executions, args.flaky_ratio, args.output)
