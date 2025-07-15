# Parallel Task Processing

Process the following task using parallel execution with sub-agents when applicable to maximize speed and efficiency.

## Instructions for Claude Code

When processing the task: `$ARGUMENTS`

1. **Task Analysis**: Analyze the task to identify components that can be executed in parallel
2. **Sub-Agent Strategy**: Use the Task tool to spawn multiple sub-agents for independent operations such as:
   - File searches across different directories
   - Multiple API calls or web fetches
   - Concurrent code analysis of different modules
   - Parallel testing of different components
   - Simultaneous documentation generation

3. **Parallel Execution Guidelines**:
   - Use multiple Task tool calls in a single response when operations are independent
   - Batch file operations (reads, searches, etc.) together
   - Process multiple bash commands concurrently when they don't depend on each other
   - Run analysis tasks on different parts of the codebase simultaneously

4. **When to Use Parallel Processing**:
   - ✅ Multiple file searches or reads
   - ✅ Independent code analysis tasks
   - ✅ Concurrent API calls or web fetches
   - ✅ Parallel testing of different features
   - ✅ Multiple bash commands with no dependencies
   - ❌ Sequential operations that depend on previous results
   - ❌ Single file edits or modifications
   - ❌ Tasks requiring specific execution order

5. **Optimization Strategy**:
   - Break down complex tasks into smaller, independent sub-tasks
   - Identify bottlenecks and parallelize around them
   - Use sub-agents to handle different aspects of the same problem
   - Coordinate results from parallel operations efficiently

Execute the task with maximum parallelization while maintaining accuracy and completeness.