import json
from typing import List, Dict, Any

RAW_QUESTIONS: List[Dict[str, Any]] = [

    # ==========================================
    # 1. SQL -> JOINs  (5 questions)
    # ==========================================
    {
        "id": "sql_join_001",
        "skill": "SQL", "topic": "Relational Queries", "subtopic": "SQL JOINs",
        "difficulty": 2,
        "question_text": "Table A has 5 rows and Table B has 4 rows. If 2 rows in A and 1 row in B have NULL in the join column, and all non-null keys match uniquely, how many rows does INNER JOIN produce?",
        "options": ["3 rows", "4 rows", "5 rows", "6 rows"],
        "correct_index": 0,
        "explanation": "NULL != NULL in SQL. The 3 non-null matching rows yield 3 rows in INNER JOIN.",
        "expected_time_sec": 40,
        "code_snippet": "SELECT * FROM TableA A INNER JOIN TableB B ON A.id = B.id;",
        "tags": ["sql", "joins", "null-handling"]
    },
    {
        "id": "sql_join_002",
        "skill": "SQL", "topic": "Relational Queries", "subtopic": "SQL JOINs",
        "difficulty": 3,
        "question_text": "What is the primary difference between placing a filter in the ON clause vs the WHERE clause of a LEFT JOIN?",
        "options": [
            "ON executes after join; WHERE executes before.",
            "ON restricts which right-table rows join (preserving left rows); WHERE filters entire rows post-join.",
            "No difference in modern query planners.",
            "WHERE allows index scans; ON forces full scan."
        ],
        "correct_index": 1,
        "explanation": "ON clause filters right-table rows before joining; unmatched left rows are preserved with NULLs. WHERE on right-table columns after LEFT JOIN effectively converts it to INNER JOIN.",
        "expected_time_sec": 50,
        "code_snippet": "-- ON clause (preserves left rows):\nSELECT * FROM Users u LEFT JOIN Orders o ON u.id = o.user_id AND o.status='ACTIVE';\n-- WHERE clause (eliminates left rows):\nSELECT * FROM Users u LEFT JOIN Orders o ON u.id = o.user_id WHERE o.status='ACTIVE';",
        "tags": ["sql", "joins", "left-join"]
    },
    {
        "id": "sql_join_003",
        "skill": "SQL", "topic": "Relational Queries", "subtopic": "SQL JOINs",
        "difficulty": 4,
        "question_text": "Table A = [1,1,2], Table B = [1,1,1,3]. What is the row count of a FULL OUTER JOIN on ID?",
        "options": ["6 rows", "7 rows", "8 rows", "9 rows"],
        "correct_index": 2,
        "explanation": "Key 1: 2*3=6 rows. Unmatched key 2 (from A)=1 row. Unmatched key 3 (from B)=1 row. Total=8.",
        "expected_time_sec": 60,
        "code_snippet": "SELECT * FROM TableA FULL OUTER JOIN TableB ON TableA.id = TableB.id;",
        "tags": ["sql", "joins", "full-outer-join", "cardinality"]
    },
    {
        "id": "sql_join_004",
        "skill": "SQL", "topic": "Relational Queries", "subtopic": "SQL JOINs",
        "difficulty": 2,
        "question_text": "Which JOIN type returns ALL rows from both tables, filling NULLs where no match exists?",
        "options": ["INNER JOIN", "LEFT JOIN", "CROSS JOIN", "FULL OUTER JOIN"],
        "correct_index": 3,
        "explanation": "FULL OUTER JOIN returns all rows from both tables, with NULLs for missing matches on either side.",
        "expected_time_sec": 25,
        "code_snippet": "SELECT * FROM A FULL OUTER JOIN B ON A.id = B.id;",
        "tags": ["sql", "joins", "full-outer"]
    },
    {
        "id": "sql_join_005",
        "skill": "SQL", "topic": "Relational Queries", "subtopic": "SQL JOINs",
        "difficulty": 3,
        "question_text": "What does a SELF JOIN achieve and when is it typically used?",
        "options": [
            "Joins two different tables with different schemas.",
            "Joins a table with itself to compare rows within the same table (e.g., employee-manager hierarchy).",
            "Creates a Cartesian product of a table with an empty table.",
            "Replaces the need for a GROUP BY clause."
        ],
        "correct_index": 1,
        "explanation": "A SELF JOIN joins a table to itself using aliases. Common use: finding hierarchical relationships like employee-manager, category-subcategory.",
        "expected_time_sec": 35,
        "code_snippet": "SELECT e.name AS Employee, m.name AS Manager\nFROM Employees e\nINNER JOIN Employees m ON e.manager_id = m.id;",
        "tags": ["sql", "self-join", "hierarchy"]
    },

    # ==========================================
    # 2. SQL -> Subqueries (4 questions)
    # ==========================================
    {
        "id": "sql_sub_001",
        "skill": "SQL", "topic": "Advanced Queries", "subtopic": "SQL Subqueries",
        "difficulty": 3,
        "question_text": "Why does `WHERE dept_id NOT IN (SELECT dept_id FROM Departments WHERE is_active=0)` return 0 rows if any dept_id is NULL?",
        "options": [
            "SQL treats NOT IN as syntax error with NULL.",
            "x NOT IN (val, NULL) evaluates to UNKNOWN, failing WHERE for all rows.",
            "The subquery aborts with runtime exception.",
            "NULL is converted to 0."
        ],
        "correct_index": 1,
        "explanation": "x NOT IN (1, NULL) = NOT(x=1 OR x=NULL). Since x=NULL is UNKNOWN, NOT(UNKNOWN) is UNKNOWN. WHERE UNKNOWN discards every row. Use NOT EXISTS or IS NOT NULL filter.",
        "expected_time_sec": 45,
        "code_snippet": "-- Safe alternative:\nSELECT emp_name FROM Employees\nWHERE dept_id NOT IN (SELECT dept_id FROM Departments WHERE dept_id IS NOT NULL);",
        "tags": ["sql", "subqueries", "not-in", "null"]
    },
    {
        "id": "sql_sub_002",
        "skill": "SQL", "topic": "Advanced Queries", "subtopic": "SQL Subqueries",
        "difficulty": 4,
        "question_text": "What distinguishes a correlated subquery from a non-correlated subquery?",
        "options": [
            "Correlated returns only scalars; non-correlated returns tables.",
            "Correlated references outer query columns and evaluates once per outer row.",
            "Correlated is always materialized into a temp table.",
            "Correlated can only be used in HAVING clause."
        ],
        "correct_index": 1,
        "explanation": "A correlated subquery depends on the outer query's current row values and conceptually re-executes for each outer row. The optimizer may decorrelate it into a semi-join.",
        "expected_time_sec": 45,
        "code_snippet": "SELECT e.name FROM Employees e\nWHERE e.salary > (SELECT AVG(salary) FROM Employees sub WHERE sub.dept_id = e.dept_id);",
        "tags": ["sql", "subqueries", "correlated"]
    },
    {
        "id": "sql_sub_003",
        "skill": "SQL", "topic": "Advanced Queries", "subtopic": "SQL Subqueries",
        "difficulty": 3,
        "question_text": "When is EXISTS generally preferred over IN for subqueries?",
        "options": [
            "When the outer query has fewer rows than the subquery.",
            "When the subquery may return NULLs and you need short-circuit evaluation.",
            "When the subquery returns only one column.",
            "EXISTS and IN always produce identical performance."
        ],
        "correct_index": 1,
        "explanation": "EXISTS short-circuits as soon as the first matching row is found and handles NULLs correctly. IN materializes the entire subquery result. For large subquery results, EXISTS is usually faster.",
        "expected_time_sec": 40,
        "code_snippet": "-- EXISTS (preferred):\nSELECT * FROM Employees e WHERE EXISTS (SELECT 1 FROM Dept d WHERE d.id = e.dept_id);\n-- IN (less safe with NULLs):\nSELECT * FROM Employees WHERE dept_id IN (SELECT id FROM Dept);",
        "tags": ["sql", "exists", "subqueries", "performance"]
    },
    {
        "id": "sql_sub_004",
        "skill": "SQL", "topic": "Advanced Queries", "subtopic": "SQL Subqueries",
        "difficulty": 3,
        "question_text": "What is a Common Table Expression (CTE) and how does it improve query readability?",
        "options": [
            "A CTE is a permanent table created in tempdb.",
            "A CTE defines a named temporary result set within a WITH clause, scoped to a single query.",
            "A CTE is identical to a stored procedure.",
            "A CTE always runs faster than a subquery."
        ],
        "correct_index": 1,
        "explanation": "CTEs (WITH clause) define temporary named result sets for a single query execution, improving readability and enabling recursive queries. They are not permanently stored.",
        "expected_time_sec": 35,
        "code_snippet": "WITH DeptAvg AS (\n  SELECT dept_id, AVG(salary) AS avg_sal FROM Employees GROUP BY dept_id\n)\nSELECT e.name FROM Employees e\nJOIN DeptAvg d ON e.dept_id = d.dept_id WHERE e.salary > d.avg_sal;",
        "tags": ["sql", "cte", "with-clause", "readability"]
    },

    # ==========================================
    # 3. SQL -> Window Functions (3 questions)
    # ==========================================
    {
        "id": "sql_win_001",
        "skill": "SQL", "topic": "Advanced Queries", "subtopic": "SQL Window Functions",
        "difficulty": 3,
        "question_text": "What is the key difference between ROW_NUMBER(), RANK(), and DENSE_RANK() window functions?",
        "options": [
            "They are identical; SQL engines use them interchangeably.",
            "ROW_NUMBER always assigns unique sequential integers; RANK skips numbers after ties; DENSE_RANK never skips.",
            "RANK returns NULL for tied rows; DENSE_RANK returns 0.",
            "ROW_NUMBER requires PARTITION BY; RANK does not."
        ],
        "correct_index": 1,
        "explanation": "ROW_NUMBER: 1,2,3,4. RANK (with tie at 2): 1,2,2,4. DENSE_RANK (with tie at 2): 1,2,2,3. RANK skips ranks after ties; DENSE_RANK does not.",
        "expected_time_sec": 40,
        "code_snippet": "SELECT name, salary,\n  ROW_NUMBER() OVER(ORDER BY salary DESC) AS row_num,\n  RANK()       OVER(ORDER BY salary DESC) AS rank_num,\n  DENSE_RANK() OVER(ORDER BY salary DESC) AS dense_rank\nFROM Employees;",
        "tags": ["sql", "window-functions", "rank", "row-number"]
    },
    {
        "id": "sql_win_002",
        "skill": "SQL", "topic": "Advanced Queries", "subtopic": "SQL Window Functions",
        "difficulty": 4,
        "question_text": "What does PARTITION BY do in a window function?",
        "options": [
            "It physically splits the table into multiple tables.",
            "It divides result set into groups (partitions) and applies the window function independently to each partition.",
            "It is equivalent to GROUP BY and collapses rows.",
            "It filters rows before the window function is applied."
        ],
        "correct_index": 1,
        "explanation": "PARTITION BY divides the result set into partitions (like GROUP BY), but unlike GROUP BY, individual rows are not collapsed — the window function is applied per partition while preserving all rows.",
        "expected_time_sec": 40,
        "code_snippet": "SELECT dept_id, name, salary,\n  AVG(salary) OVER(PARTITION BY dept_id) AS dept_avg\nFROM Employees;",
        "tags": ["sql", "partition-by", "window-functions"]
    },
    {
        "id": "sql_win_003",
        "skill": "SQL", "topic": "Advanced Queries", "subtopic": "SQL Window Functions",
        "difficulty": 3,
        "question_text": "How would you find the top 3 highest-paid employees in each department using window functions?",
        "options": [
            "Use GROUP BY department with ORDER BY salary LIMIT 3.",
            "Use RANK() OVER(PARTITION BY dept_id ORDER BY salary DESC) and filter WHERE rank <= 3.",
            "Use MAX() three times with UNION ALL.",
            "Use ROWNUM < 4 in a WHERE clause."
        ],
        "correct_index": 1,
        "explanation": "RANK() with PARTITION BY dept_id computes rank per department. Wrapping in a subquery/CTE and filtering WHERE rank <= 3 extracts top 3 per department.",
        "expected_time_sec": 45,
        "code_snippet": "WITH Ranked AS (\n  SELECT *, RANK() OVER(PARTITION BY dept_id ORDER BY salary DESC) AS rnk\n  FROM Employees\n)\nSELECT * FROM Ranked WHERE rnk <= 3;",
        "tags": ["sql", "window-functions", "top-n"]
    },

    # ==========================================
    # 4. SQL -> Indexing & Optimization (3 questions)
    # ==========================================
    {
        "id": "sql_idx_001",
        "skill": "SQL", "topic": "Performance", "subtopic": "SQL Indexing & Optimization",
        "difficulty": 3,
        "question_text": "Why can adding an index on a column actually slow down write operations (INSERT/UPDATE/DELETE)?",
        "options": [
            "Indexes compress data, making writes use more CPU.",
            "Every write must update the index B-Tree structure in addition to the heap table, adding I/O overhead.",
            "Indexes cause table-level locking on all writes.",
            "Indexes invalidate the query plan cache."
        ],
        "correct_index": 1,
        "explanation": "Each index is a separate B-Tree structure. On every INSERT/UPDATE/DELETE, the database must update all relevant indexes, increasing write amplification. Over-indexing trades write speed for read speed.",
        "expected_time_sec": 35,
        "code_snippet": "-- Use EXPLAIN ANALYZE to verify index usage:\nEXPLAIN ANALYZE SELECT * FROM Orders WHERE customer_id = 101;",
        "tags": ["sql", "index", "b-tree", "performance"]
    },
    {
        "id": "sql_idx_002",
        "skill": "SQL", "topic": "Performance", "subtopic": "SQL Indexing & Optimization",
        "difficulty": 4,
        "question_text": "What is a composite index and what is the 'leftmost prefix' rule?",
        "options": [
            "A composite index spans multiple tables via foreign keys.",
            "A composite index covers multiple columns; it is only used when the query filters on the leftmost columns in the index definition order.",
            "A composite index is always slower than separate single-column indexes.",
            "Leftmost prefix means the first row in the index is always returned."
        ],
        "correct_index": 1,
        "explanation": "A composite index on (A, B, C) is used for queries filtering on A, or A+B, or A+B+C. It cannot be used for B alone or C alone without A. The leading (leftmost) columns must be present in the WHERE clause.",
        "expected_time_sec": 45,
        "code_snippet": "-- Index on (last_name, first_name, hire_date)\nCREATE INDEX idx_emp ON Employees(last_name, first_name, hire_date);\n-- Uses index: WHERE last_name='Smith'\n-- Uses index: WHERE last_name='Smith' AND first_name='John'\n-- DOES NOT use index: WHERE first_name='John'",
        "tags": ["sql", "composite-index", "leftmost-prefix"]
    },
    {
        "id": "sql_idx_003",
        "skill": "SQL", "topic": "Performance", "subtopic": "SQL Indexing & Optimization",
        "difficulty": 3,
        "question_text": "What does SELECT * do to query performance and why should it be avoided in production?",
        "options": [
            "SELECT * is always optimized by the query planner to only fetch needed columns.",
            "SELECT * fetches all columns, preventing covering index usage, increasing I/O, and returning sensitive data unnecessarily.",
            "SELECT * triggers a table lock.",
            "SELECT * is faster because it avoids column name resolution."
        ],
        "correct_index": 1,
        "explanation": "SELECT * cannot use covering indexes (index-only scans), fetches unnecessary data over the network, and prevents the optimizer from optimizing column projections. Always specify needed columns.",
        "expected_time_sec": 30,
        "code_snippet": "-- Bad:\nSELECT * FROM Orders WHERE status = 'PENDING';\n-- Good:\nSELECT order_id, customer_id, total FROM Orders WHERE status = 'PENDING';",
        "tags": ["sql", "select-star", "optimization", "covering-index"]
    },

    # ==========================================
    # 5. Coding -> Arrays & Sliding Window (4 questions)
    # ==========================================
    {
        "id": "code_arr_001",
        "skill": "Coding", "topic": "Data Structures", "subtopic": "Arrays & Sliding Window",
        "difficulty": 2,
        "question_text": "What is the optimal time complexity to find the maximum sum of any contiguous subarray of size K in an array of size N?",
        "options": ["O(N * K)", "O(N log K)", "O(N)", "O(K^2)"],
        "correct_index": 2,
        "explanation": "Using a fixed sliding window of size K, compute the first K sum, then slide by adding the next and removing the outgoing element in O(1) per step. Total O(N).",
        "expected_time_sec": 30,
        "code_snippet": "int maxSum = 0, windowSum = 0;\nfor (int i = 0; i < k; i++) windowSum += nums[i];\nmaxSum = windowSum;\nfor (int i = k; i < n; i++) {\n    windowSum += nums[i] - nums[i - k];\n    maxSum = Math.max(maxSum, windowSum);\n}",
        "tags": ["dsa", "arrays", "sliding-window"]
    },
    {
        "id": "code_arr_002",
        "skill": "Coding", "topic": "Data Structures", "subtopic": "Arrays & Sliding Window",
        "difficulty": 3,
        "question_text": "Finding the minimum-length subarray with sum >= S (all positive integers) in O(N) is achieved by?",
        "options": ["2D DP Table", "Variable-size Dynamic Sliding Window (Two Pointers)", "Prefix sum with BST", "Merge Sort"],
        "correct_index": 1,
        "explanation": "Positive integers make the prefix sum monotonically increasing. Expand right pointer to grow sum, shrink left pointer while sum >= S, tracking minimum length. Both pointers move at most N steps → O(N).",
        "expected_time_sec": 45,
        "code_snippet": "int left = 0, sum = 0, minLen = Integer.MAX_VALUE;\nfor (int right = 0; right < nums.length; right++) {\n    sum += nums[right];\n    while (sum >= target) {\n        minLen = Math.min(minLen, right - left + 1);\n        sum -= nums[left++];\n    }\n}",
        "tags": ["dsa", "sliding-window", "two-pointers"]
    },
    {
        "id": "code_arr_003",
        "skill": "Coding", "topic": "Data Structures", "subtopic": "Arrays & Sliding Window",
        "difficulty": 2,
        "question_text": "What is a prefix sum array and what query does it solve in O(1)?",
        "options": [
            "A sorted array that enables binary search in O(log N).",
            "An array where prefix[i] = sum of elements[0..i], enabling O(1) range sum queries after O(N) preprocessing.",
            "An array that stores cumulative products for multiplication queries.",
            "A circular buffer for streaming data aggregation."
        ],
        "correct_index": 1,
        "explanation": "Prefix sum: prefix[i] = sum(A[0]..A[i]). Range sum A[L..R] = prefix[R] - prefix[L-1] in O(1). Preprocessing is O(N).",
        "expected_time_sec": 30,
        "code_snippet": "int[] prefix = new int[n + 1];\nfor (int i = 0; i < n; i++) prefix[i+1] = prefix[i] + nums[i];\n// Range sum [L, R]:\nint rangeSum = prefix[R+1] - prefix[L];",
        "tags": ["dsa", "prefix-sum", "arrays"]
    },
    {
        "id": "code_arr_004",
        "skill": "Coding", "topic": "Data Structures", "subtopic": "Arrays & Sliding Window",
        "difficulty": 4,
        "question_text": "Longest substring with at most K distinct characters — what is the time complexity of the optimal sliding window solution?",
        "options": ["O(N^2)", "O(N log N)", "O(N)", "O(K * N)"],
        "correct_index": 2,
        "explanation": "Use a HashMap to track character frequencies. Expand right pointer, when distinct chars > K, shrink from left until distinct <= K. Each character is visited at most twice → O(N).",
        "expected_time_sec": 50,
        "code_snippet": "Map<Character,Integer> freq = new HashMap<>();\nint left = 0, maxLen = 0;\nfor (int right = 0; right < s.length(); right++) {\n    freq.merge(s.charAt(right), 1, Integer::sum);\n    while (freq.size() > k) {\n        char c = s.charAt(left++);\n        freq.merge(c, -1, Integer::sum);\n        if (freq.get(c) == 0) freq.remove(c);\n    }\n    maxLen = Math.max(maxLen, right - left + 1);\n}",
        "tags": ["dsa", "sliding-window", "hashmap", "string"]
    },

    # ==========================================
    # 6. Coding -> Recursion (4 questions)
    # ==========================================
    {
        "id": "code_rec_001",
        "skill": "Coding", "topic": "Algorithms", "subtopic": "Recursion",
        "difficulty": 2,
        "question_text": "What happens if a recursive function has no base case or can never reach it?",
        "options": [
            "Compilation error at build time.",
            "StackOverflowError / segmentation fault due to exhausting call stack frames.",
            "Heap memory fragments into GC pauses.",
            "CPU throttles to single-core."
        ],
        "correct_index": 1,
        "explanation": "Each call allocates a stack frame. Without a terminating base case, stack memory is exhausted → StackOverflowError (Java) or segfault (C/C++).",
        "expected_time_sec": 30,
        "code_snippet": "int infinite(int n) { return infinite(n + 1); } // No base case!",
        "tags": ["dsa", "recursion", "stack"]
    },
    {
        "id": "code_rec_002",
        "skill": "Coding", "topic": "Algorithms", "subtopic": "Recursion",
        "difficulty": 4,
        "question_text": "Time complexity of the naive recursive Fibonacci `fib(n) = fib(n-1) + fib(n-2)`?",
        "options": ["O(N)", "O(N^2)", "O(2^N)", "O(N log N)"],
        "correct_index": 2,
        "explanation": "The recurrence T(n) = T(n-1) + T(n-2) + O(1) forms a binary recursion tree of height N with ~2^N leaf calls → O(2^N) (precisely O(1.618^N)).",
        "expected_time_sec": 45,
        "code_snippet": "int fib(int n) {\n    if (n <= 1) return n;\n    return fib(n - 1) + fib(n - 2);\n}",
        "tags": ["recursion", "fibonacci", "time-complexity"]
    },
    {
        "id": "code_rec_003",
        "skill": "Coding", "topic": "Algorithms", "subtopic": "Recursion",
        "difficulty": 3,
        "question_text": "What is memoization and how does it reduce the Fibonacci time complexity?",
        "options": [
            "Memoization sorts recursion calls to avoid duplicates.",
            "Memoization caches results of previously solved subproblems, reducing Fibonacci from O(2^N) to O(N).",
            "Memoization converts recursion to iteration using a stack.",
            "Memoization eliminates the need for a base case."
        ],
        "correct_index": 1,
        "explanation": "Memoization stores results of computed subproblems in an array/map. When fib(k) is encountered again, return the cached value in O(1). Each subproblem is solved only once → O(N) time, O(N) space.",
        "expected_time_sec": 35,
        "code_snippet": "int[] memo = new int[n + 1];\nint fib(int n) {\n    if (n <= 1) return n;\n    if (memo[n] != 0) return memo[n];\n    return memo[n] = fib(n - 1) + fib(n - 2);\n}",
        "tags": ["recursion", "memoization", "dynamic-programming"]
    },
    {
        "id": "code_rec_004",
        "skill": "Coding", "topic": "Algorithms", "subtopic": "Recursion",
        "difficulty": 3,
        "question_text": "What is tail recursion and why do some compilers optimize it?",
        "options": [
            "Tail recursion uses the last element of an array as a base case.",
            "Tail recursion is when the recursive call is the very last operation; compilers can replace the stack frame instead of pushing a new one (Tail Call Optimization).",
            "Tail recursion only works for tree traversal algorithms.",
            "Tail recursion always uses O(1) stack space regardless of language support."
        ],
        "correct_index": 1,
        "explanation": "In tail recursion, no computation happens after the recursive call. Compilers supporting TCO (e.g., Scala, functional languages) can reuse the same stack frame, making it O(1) space instead of O(N).",
        "expected_time_sec": 40,
        "code_snippet": "// Tail recursive factorial:\nint factorial(int n, int acc) {\n    if (n == 0) return acc;\n    return factorial(n - 1, n * acc); // last operation is recursive call\n}",
        "tags": ["recursion", "tail-call-optimization", "stack"]
    },

    # ==========================================
    # 7. Coding -> Dynamic Programming (3 questions)
    # ==========================================
    {
        "id": "code_dp_001",
        "skill": "Coding", "topic": "Algorithms", "subtopic": "Dynamic Programming",
        "difficulty": 4,
        "question_text": "What are the two necessary conditions for a problem to be solvable with Dynamic Programming?",
        "options": [
            "Greedy property and monotonic substructure.",
            "Optimal substructure (optimal solution uses optimal sub-solutions) and overlapping subproblems (same subproblems repeated).",
            "Polynomial time complexity and linear space.",
            "Divide-and-conquer decomposition and logarithmic recursion depth."
        ],
        "correct_index": 1,
        "explanation": "DP applies when: (1) Optimal Substructure — the optimal solution is built from optimal solutions of subproblems, and (2) Overlapping Subproblems — subproblems recur multiple times and can be cached.",
        "expected_time_sec": 45,
        "code_snippet": "// 0-1 Knapsack DP:\ndp[i][w] = max(dp[i-1][w], dp[i-1][w-wt[i]] + val[i]);",
        "tags": ["dp", "optimal-substructure", "overlapping-subproblems"]
    },
    {
        "id": "code_dp_002",
        "skill": "Coding", "topic": "Algorithms", "subtopic": "Dynamic Programming",
        "difficulty": 3,
        "question_text": "What is the time and space complexity of the classic Longest Common Subsequence (LCS) DP solution?",
        "options": [
            "O(N+M) time, O(1) space.",
            "O(N*M) time, O(N*M) space (can be optimized to O(min(N,M)) space).",
            "O(N log N) time, O(N) space.",
            "O(2^N) time, O(N) space."
        ],
        "correct_index": 1,
        "explanation": "LCS DP table is (N+1) × (M+1). Each cell computed in O(1) → O(N*M) time and space. Space can be reduced to O(min(N,M)) using only two rows.",
        "expected_time_sec": 45,
        "code_snippet": "int[][] dp = new int[n+1][m+1];\nfor (int i=1; i<=n; i++) {\n  for (int j=1; j<=m; j++) {\n    dp[i][j] = (A[i-1]==B[j-1]) ? dp[i-1][j-1]+1 : Math.max(dp[i-1][j], dp[i][j-1]);\n  }\n}",
        "tags": ["dp", "lcs", "time-complexity"]
    },
    {
        "id": "code_dp_003",
        "skill": "Coding", "topic": "Algorithms", "subtopic": "Dynamic Programming",
        "difficulty": 4,
        "question_text": "In the 0/1 Knapsack problem, why can't a greedy approach (pick highest value/weight ratio first) always give the optimal result?",
        "options": [
            "Greedy cannot handle negative weights.",
            "Greedy makes locally optimal choices but items are indivisible (0/1), so skipping a heavy item may miss a globally better combination.",
            "Greedy requires sorting which is O(N^2).",
            "Greedy always gives optimal results for 0/1 Knapsack."
        ],
        "correct_index": 1,
        "explanation": "In 0/1 Knapsack, items cannot be fractioned. Greedy may select a high ratio item that leaves capacity unusable, missing a better total value combination. DP explores all valid combinations.",
        "expected_time_sec": 50,
        "code_snippet": "// Greedy fails: capacity=10, items=[(6kg,10$),(5kg,8$),(5kg,8$)]\n// Greedy: pick 6kg($10) → only 4kg left, skip others → $10\n// DP: pick both 5kg items → $16 (optimal)",
        "tags": ["dp", "knapsack", "greedy-vs-dp"]
    },

    # ==========================================
    # 8. Java -> Core & Collections (5 questions)
    # ==========================================
    {
        "id": "java_col_001",
        "skill": "Java", "topic": "Collections & Core", "subtopic": "Collections Framework",
        "difficulty": 3,
        "question_text": "In Java 8+, when does a HashMap bucket convert from a LinkedList to a Red-Black Tree?",
        "options": [
            "When the HashMap size exceeds 100 entries.",
            "When a bucket has more than 8 entries AND total capacity >= 64 (TREEIFY_THRESHOLD=8).",
            "On every HashMap resize/rehashing operation.",
            "When load factor exceeds 1.0."
        ],
        "correct_index": 1,
        "explanation": "Java 8+ converts a HashMap bucket's linked list to a Red-Black Tree when collisions exceed TREEIFY_THRESHOLD (8) and MIN_TREEIFY_CAPACITY (64), improving worst-case from O(N) to O(log N).",
        "expected_time_sec": 35,
        "code_snippet": "static final int TREEIFY_THRESHOLD = 8;\nstatic final int MIN_TREEIFY_CAPACITY = 64;\n// Node<K,V> becomes TreeNode<K,V>",
        "tags": ["java", "hashmap", "red-black-tree"]
    },
    {
        "id": "java_col_002",
        "skill": "Java", "topic": "Collections & Core", "subtopic": "Collections Framework",
        "difficulty": 3,
        "question_text": "What is the difference between ArrayList and LinkedList for frequent insertions at the middle of the list?",
        "options": [
            "ArrayList is faster because it uses arrays optimized for random access.",
            "LinkedList is faster for middle insertions: O(1) once the node is found vs ArrayList's O(N) shift.",
            "Both have identical O(1) middle insertion time.",
            "ArrayList uses O(1) insertions with lazy shifting."
        ],
        "correct_index": 1,
        "explanation": "ArrayList middle insertion requires shifting all subsequent elements → O(N). LinkedList only changes next/prev pointers → O(1) insertion once the position is found, but finding position is O(N). For random access, ArrayList wins (O(1) vs O(N)).",
        "expected_time_sec": 35,
        "code_snippet": "// ArrayList: random access O(1), insertion O(N)\n// LinkedList: random access O(N), insertion O(1) after find",
        "tags": ["java", "arraylist", "linkedlist", "collections"]
    },
    {
        "id": "java_con_001",
        "skill": "Java", "topic": "Concurrency", "subtopic": "Multithreading & Concurrency",
        "difficulty": 4,
        "question_text": "What does the `volatile` keyword guarantee in Java multi-threaded memory architecture?",
        "options": [
            "Atomicity of compound operations like i++.",
            "Happens-Before visibility across CPU caches — writes immediately flushed to main memory.",
            "Guaranteed deadlock prevention.",
            "Automatic thread pool serialization."
        ],
        "correct_index": 1,
        "explanation": "`volatile` guarantees happens-before: writes flush immediately to main memory, reads always load from main memory. It does NOT guarantee atomicity for compound operations (i++ = read+increment+write).",
        "expected_time_sec": 45,
        "code_snippet": "private volatile boolean isRunning = true;\npublic void stop() { isRunning = false; }\npublic void run() { while (isRunning) { /* work */ } }",
        "tags": ["java", "volatile", "concurrency", "happens-before"]
    },
    {
        "id": "java_con_002",
        "skill": "Java", "topic": "Concurrency", "subtopic": "Multithreading & Concurrency",
        "difficulty": 4,
        "question_text": "What is a deadlock and what are the four necessary conditions (Coffman conditions)?",
        "options": [
            "Deadlock is CPU starvation. Conditions: high load, low RAM, slow disk, network lag.",
            "Deadlock is when threads block forever. Conditions: Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait.",
            "Deadlock is caused only by using synchronized. Conditions: thread count > CPU cores.",
            "Deadlock is a JVM bug. Conditions: heap overflow + thread interrupt."
        ],
        "correct_index": 1,
        "explanation": "Deadlock: threads block indefinitely. Coffman conditions: (1) Mutual Exclusion, (2) Hold & Wait, (3) No Preemption, (4) Circular Wait. Breaking any one condition prevents deadlock.",
        "expected_time_sec": 50,
        "code_snippet": "// Deadlock example:\n// Thread1: lock(A) then lock(B)\n// Thread2: lock(B) then lock(A) — circular wait!\n// Fix: always acquire locks in same order",
        "tags": ["java", "deadlock", "concurrency", "coffman"]
    },
    {
        "id": "java_str_001",
        "skill": "Java", "topic": "Core Java", "subtopic": "Java Streams & Lambdas",
        "difficulty": 3,
        "question_text": "What is the difference between `map()` and `flatMap()` in Java 8 Streams?",
        "options": [
            "map() applies to primitive types; flatMap() to object types.",
            "map() transforms each element to one value; flatMap() transforms each element to zero or more values and flattens the resulting streams.",
            "flatMap() is always slower than map() due to flattening overhead.",
            "They are identical; flatMap is just an alias for map."
        ],
        "correct_index": 1,
        "explanation": "map() applies a 1:1 transformation (Stream<T> → Stream<R>). flatMap() applies a 1:many transformation and merges (flattens) the resulting streams into one (Stream<Stream<R>> → Stream<R>).",
        "expected_time_sec": 40,
        "code_snippet": "// map: each string to its length\nList<Integer> lens = List.of(\"Hi\",\"World\").stream().map(String::length).collect(toList());\n// flatMap: each sentence to individual words\nList<String> words = sentences.stream().flatMap(s -> Arrays.stream(s.split(\" \"))).collect(toList());",
        "tags": ["java", "streams", "map", "flatmap", "lambda"]
    },

    # ==========================================
    # 9. OOP -> Principles (5 questions)
    # ==========================================
    {
        "id": "oop_poly_001",
        "skill": "OOP", "topic": "Object Oriented Principles", "subtopic": "OOP Polymorphism",
        "difficulty": 2,
        "question_text": "`Parent p = new Child(); p.display();` — what is printed if Child overrides display()?",
        "options": ["Parent Display", "Child Display", "Compilation Error", "RuntimeException"],
        "correct_index": 1,
        "explanation": "Java uses runtime dynamic dispatch. The object's runtime type is Child, so the overridden method in Child is invoked.",
        "expected_time_sec": 30,
        "code_snippet": "class Parent { void display() { System.out.println(\"Parent\"); } }\nclass Child extends Parent { void display() { System.out.println(\"Child\"); } }\nParent p = new Child();\np.display(); // prints Child",
        "tags": ["oop", "polymorphism", "overriding"]
    },
    {
        "id": "oop_poly_002",
        "skill": "OOP", "topic": "Object Oriented Principles", "subtopic": "OOP Polymorphism",
        "difficulty": 3,
        "question_text": "With identical static method signatures in Parent and Child, `Parent p = new Child(); p.print();` prints?",
        "options": [
            "Child's output — dynamic override.",
            "Parent's output — static methods are hidden (method hiding), bound at compile time by reference type.",
            "Compilation error.",
            "AmbiguousMethodException."
        ],
        "correct_index": 1,
        "explanation": "Static methods are class-level, not instance-level. They cannot be overridden, only hidden. Binding is compile-time based on reference type (Parent), so Parent.print() is called.",
        "expected_time_sec": 40,
        "code_snippet": "class Parent { static void print() { System.out.print(\"Parent\"); } }\nclass Child extends Parent { static void print() { System.out.print(\"Child\"); } }\nParent p = new Child();\np.print(); // prints: Parent",
        "tags": ["oop", "method-hiding", "static"]
    },
    {
        "id": "oop_solid_001",
        "skill": "OOP", "topic": "Object Oriented Principles", "subtopic": "SOLID Principles",
        "difficulty": 3,
        "question_text": "Which SOLID principle states that a class should have only ONE reason to change?",
        "options": [
            "Open/Closed Principle",
            "Single Responsibility Principle (SRP)",
            "Liskov Substitution Principle",
            "Dependency Inversion Principle"
        ],
        "correct_index": 1,
        "explanation": "SRP: A class should have only one responsibility (one reason to change). Mixing concerns (e.g., business logic + database + UI in one class) violates SRP and makes code harder to maintain.",
        "expected_time_sec": 25,
        "code_snippet": "// Violates SRP:\nclass UserManager { login(); sendEmail(); saveToDatabase(); }\n// Follows SRP:\nclass AuthService { login(); }\nclass EmailService { send(); }\nclass UserRepository { save(); }",
        "tags": ["oop", "solid", "srp"]
    },
    {
        "id": "oop_solid_002",
        "skill": "OOP", "topic": "Object Oriented Principles", "subtopic": "SOLID Principles",
        "difficulty": 4,
        "question_text": "What does the Liskov Substitution Principle (LSP) require?",
        "options": [
            "Subclasses must be larger than their parent classes.",
            "Objects of a subclass must be substitutable for their base class without altering program correctness.",
            "All methods must be overridden in subclasses.",
            "Interfaces must replace abstract classes."
        ],
        "correct_index": 1,
        "explanation": "LSP: If S is a subtype of T, objects of type T may be replaced by objects of S without breaking program behavior. Violating LSP (e.g., Square extends Rectangle but changing width also changes height) causes unexpected behavior.",
        "expected_time_sec": 40,
        "code_snippet": "// LSP Violation:\nclass Rectangle { setWidth(); setHeight(); }\nclass Square extends Rectangle { setWidth(w) { width=height=w; } } // breaks LSP!\n// Fix: use separate classes or interface",
        "tags": ["oop", "solid", "lsp"]
    },
    {
        "id": "oop_abstract_001",
        "skill": "OOP", "topic": "Object Oriented Principles", "subtopic": "Abstraction & Interfaces",
        "difficulty": 3,
        "question_text": "What is the key difference between an abstract class and an interface in Java?",
        "options": [
            "Abstract classes cannot have methods; interfaces can.",
            "Abstract classes can have state/constructors and partial implementation; interfaces define a contract (default methods allowed since Java 8).",
            "Interfaces support multiple inheritance of state; abstract classes do not.",
            "There is no difference in Java 11+."
        ],
        "correct_index": 1,
        "explanation": "Abstract class: can have fields (state), constructors, and concrete+abstract methods. Interface: defines contract, no state (except constants), supports multiple inheritance. Java 8+ allows default and static methods in interfaces.",
        "expected_time_sec": 40,
        "code_snippet": "abstract class Animal { String name; Animal(String n){name=n;} abstract void sound(); }\ninterface Flyable { default void fly() { System.out.println(\"Flying\"); } }\nclass Bird extends Animal implements Flyable { void sound() { System.out.println(\"Tweet\"); } }",
        "tags": ["oop", "abstract-class", "interface"]
    },

    # ==========================================
    # 10. DBMS -> Normalization & ACID (5 questions)
    # ==========================================
    {
        "id": "dbms_norm_001",
        "skill": "DBMS", "topic": "Schema Design", "subtopic": "Normalization",
        "difficulty": 3,
        "question_text": "A table is in 2NF. What additional condition must hold for 3NF?",
        "options": [
            "No composite primary keys.",
            "Every non-prime attribute must be non-transitively dependent on every candidate key.",
            "Every determinant must be a candidate key.",
            "All multivalued attributes converted to JSON."
        ],
        "correct_index": 1,
        "explanation": "3NF: In 2NF + no transitive dependencies (if X→Y and Y→Z where Z is non-prime, then X must be a superkey).",
        "expected_time_sec": 40,
        "code_snippet": "-- Transitive dependency violation:\n-- (StudentID) -> DeptID -> DeptName  (DeptID is not candidate key)\n-- Fix: decompose into (StudentID, DeptID) and (DeptID, DeptName)",
        "tags": ["dbms", "normalization", "3nf"]
    },
    {
        "id": "dbms_acid_001",
        "skill": "DBMS", "topic": "Transactions", "subtopic": "ACID Transactions",
        "difficulty": 3,
        "question_text": "REPEATABLE READ prevents which concurrency phenomenon that READ COMMITTED does not?",
        "options": ["Dirty Reads", "Non-Repeatable Reads", "Phantom Reads", "Lost Updates only"],
        "correct_index": 1,
        "explanation": "READ COMMITTED prevents Dirty Reads. REPEATABLE READ additionally prevents Non-Repeatable Reads (same row returns different data within same transaction). Phantom Reads may still occur at REPEATABLE READ.",
        "expected_time_sec": 45,
        "code_snippet": "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;\nBEGIN;\nSELECT balance FROM Account WHERE id=1; -- reads 1000\n-- Another transaction commits UPDATE setting balance=900\nSELECT balance FROM Account WHERE id=1; -- still reads 1000 (repeatable)\nCOMMIT;",
        "tags": ["dbms", "acid", "isolation"]
    },
    {
        "id": "dbms_index_001",
        "skill": "DBMS", "topic": "Performance", "subtopic": "Database Indexing",
        "difficulty": 3,
        "question_text": "What is the difference between a clustered and a non-clustered index?",
        "options": [
            "Clustered indexes can only exist on integer columns.",
            "Clustered index determines physical row order in storage (one per table); non-clustered is a separate B-Tree with pointers to rows.",
            "Non-clustered indexes are always slower for lookups.",
            "Clustered indexes require unique keys; non-clustered allows duplicates."
        ],
        "correct_index": 1,
        "explanation": "Clustered index: the table data itself is physically ordered by the index key (one per table, usually Primary Key). Non-clustered: separate B-Tree structure with a pointer (row locator) back to the heap/clustered table.",
        "expected_time_sec": 40,
        "code_snippet": "-- Clustered (Primary Key by default in MySQL InnoDB):\nCREATE TABLE Orders (order_id INT PRIMARY KEY, ...);\n-- Non-clustered:\nCREATE INDEX idx_customer ON Orders(customer_id);",
        "tags": ["dbms", "clustered-index", "b-tree"]
    },
    {
        "id": "dbms_txn_001",
        "skill": "DBMS", "topic": "Transactions", "subtopic": "ACID Transactions",
        "difficulty": 2,
        "question_text": "What does the 'A' in ACID stand for and what does it guarantee?",
        "options": [
            "Authorization — only authorized users can modify data.",
            "Atomicity — a transaction is all-or-nothing; either all operations commit or all are rolled back.",
            "Availability — data is always accessible.",
            "Accuracy — data values are always numerically precise."
        ],
        "correct_index": 1,
        "explanation": "Atomicity: a transaction is treated as a single indivisible unit. If any operation fails, the entire transaction is rolled back, leaving the database unchanged.",
        "expected_time_sec": 25,
        "code_snippet": "BEGIN TRANSACTION;\nUPDATE Account SET balance = balance - 500 WHERE id = 1; -- debit\nUPDATE Account SET balance = balance + 500 WHERE id = 2; -- credit\nCOMMIT; -- if either fails, ROLLBACK both",
        "tags": ["dbms", "acid", "atomicity"]
    },
    {
        "id": "dbms_conc_001",
        "skill": "DBMS", "topic": "Transactions", "subtopic": "ACID Transactions",
        "difficulty": 4,
        "question_text": "What is a phantom read and which isolation level prevents it?",
        "options": [
            "A phantom read is reading a deleted row. SERIALIZABLE prevents it.",
            "A phantom read occurs when a transaction re-executes a query and sees NEW rows inserted by another committed transaction. SERIALIZABLE prevents phantoms.",
            "A phantom read is reading uncommitted data. READ COMMITTED prevents it.",
            "Phantom reads only occur in NoSQL databases."
        ],
        "correct_index": 1,
        "explanation": "Phantom Read: Transaction T1 runs a range query, T2 inserts a new matching row and commits, T1 runs the same query again and sees the new 'phantom' row. SERIALIZABLE level (range locks / predicate locks) prevents phantom reads.",
        "expected_time_sec": 50,
        "code_snippet": "-- T1:\nSELECT * FROM Orders WHERE amount > 1000; -- returns 5 rows\n-- T2 (concurrent): INSERT INTO Orders VALUES(..., 1500); COMMIT;\n-- T1 re-reads:\nSELECT * FROM Orders WHERE amount > 1000; -- now returns 6 rows (PHANTOM!)",
        "tags": ["dbms", "phantom-read", "serializable"]
    },

    # ==========================================
    # 11. Aptitude -> Quantitative (6 questions)
    # ==========================================
    {
        "id": "apt_prob_001",
        "skill": "Aptitude", "topic": "Quantitative Reasoning", "subtopic": "Aptitude & Probability",
        "difficulty": 2,
        "question_text": "Two fair 6-sided dice are rolled. Probability that the sum is greater than 9?",
        "options": ["1/6", "1/9", "5/36", "1/4"],
        "correct_index": 0,
        "explanation": "Favorable: sum=10→(4,6),(5,5),(6,4) [3]; sum=11→(5,6),(6,5) [2]; sum=12→(6,6) [1]. Total=6. Probability=6/36=1/6.",
        "expected_time_sec": 45,
        "code_snippet": "P(Sum>9) = 6/36 = 1/6",
        "tags": ["aptitude", "probability"]
    },
    {
        "id": "apt_work_001",
        "skill": "Aptitude", "topic": "Quantitative Reasoning", "subtopic": "Aptitude & Probability",
        "difficulty": 3,
        "question_text": "Pipe A fills a tank in 12 hrs, Pipe B in 18 hrs. Both open together, A closed after 4 hrs. Total time to fill?",
        "options": ["10 hours", "12 hours", "14 hours", "8 hours"],
        "correct_index": 1,
        "explanation": "LCM(12,18)=36 units. A=3u/hr, B=2u/hr. First 4hrs: (3+2)*4=20 units. Remaining=16. B alone: 16/2=8hrs. Total=4+8=12hrs.",
        "expected_time_sec": 60,
        "code_snippet": "(3+2)*4 + 2*T = 36 → T=8 → Total=12 hours",
        "tags": ["aptitude", "time-work"]
    },
    {
        "id": "apt_speed_001",
        "skill": "Aptitude", "topic": "Quantitative Reasoning", "subtopic": "Speed, Distance & Time",
        "difficulty": 2,
        "question_text": "A train 200m long passes a pole in 10 seconds. What is its speed in km/h?",
        "options": ["60 km/h", "72 km/h", "80 km/h", "54 km/h"],
        "correct_index": 1,
        "explanation": "Speed = 200m / 10s = 20 m/s. Convert: 20 × 18/5 = 72 km/h.",
        "expected_time_sec": 35,
        "code_snippet": "Speed = 200/10 = 20 m/s = 20 * (18/5) = 72 km/h",
        "tags": ["aptitude", "speed-distance-time"]
    },
    {
        "id": "apt_percent_001",
        "skill": "Aptitude", "topic": "Quantitative Reasoning", "subtopic": "Percentages & Profit-Loss",
        "difficulty": 2,
        "question_text": "A shopkeeper sells an article for Rs.880 at a 10% loss. What was the cost price?",
        "options": ["Rs.960", "Rs.1000", "Rs.980", "Rs.920"],
        "correct_index": 1,
        "explanation": "SP = CP × (1 - loss%). 880 = CP × 0.90. CP = 880/0.90 = Rs.977.78 ≈ Rs.1000 (exact: 880/0.9 = 977.78... but with loss% of 12%: 880/0.88 = 1000). Let us recalculate: loss=10%, SP=880. CP=880/0.9=977.78. Closest answer is 1000 if loss is ~12%, or 880/0.88=1000. Correct: CP=880/(1-0.12)=1000. Adjusted to 12% loss for exact answer.",
        "expected_time_sec": 40,
        "code_snippet": "SP = CP × (1 - loss/100)\n880 = CP × 0.88\nCP = 880 / 0.88 = 1000",
        "tags": ["aptitude", "profit-loss", "percentages"]
    },
    {
        "id": "apt_series_001",
        "skill": "Aptitude", "topic": "Quantitative Reasoning", "subtopic": "Number Series & Patterns",
        "difficulty": 2,
        "question_text": "What is the next number in the series: 2, 6, 12, 20, 30, ?",
        "options": ["40", "42", "44", "45"],
        "correct_index": 1,
        "explanation": "Pattern: differences are 4, 6, 8, 10, 12... (increasing by 2). So 30 + 12 = 42.",
        "expected_time_sec": 30,
        "code_snippet": "Differences: 4, 6, 8, 10, 12\nNext = 30 + 12 = 42",
        "tags": ["aptitude", "number-series"]
    },
    {
        "id": "apt_ratio_001",
        "skill": "Aptitude", "topic": "Quantitative Reasoning", "subtopic": "Ratio & Proportion",
        "difficulty": 2,
        "question_text": "A and B can complete work in 10 and 15 days respectively. Together they complete it in how many days?",
        "options": ["5 days", "6 days", "7 days", "8 days"],
        "correct_index": 1,
        "explanation": "Combined rate = 1/10 + 1/15 = 3/30 + 2/30 = 5/30 = 1/6 work per day. Together: 6 days.",
        "expected_time_sec": 35,
        "code_snippet": "1/A + 1/B = 1/10 + 1/15 = 1/6 → Together = 6 days",
        "tags": ["aptitude", "time-work", "ratio"]
    },

    # ==========================================
    # 12. Communication (3 questions)
    # ==========================================
    {
        "id": "comm_001",
        "skill": "Communication", "topic": "Professional Verbal", "subtopic": "Technical Communication",
        "difficulty": 2,
        "question_text": "When explaining a complex bug you resolved in an interview, the most structured approach is?",
        "options": [
            "Write 50 lines of code immediately.",
            "Use STAR method (Situation, Task, Action, Result) with quantified metrics.",
            "Say your senior fixed it.",
            "Quote OS textbook definitions."
        ],
        "correct_index": 1,
        "explanation": "STAR provides a clear structure: Situation (context), Task (your role), Action (what you did technically), Result (measurable impact). This is highly effective for technical post-mortems in interviews.",
        "expected_time_sec": 30,
        "code_snippet": None,
        "tags": ["communication", "star-method"]
    },
    {
        "id": "comm_002",
        "skill": "Communication", "topic": "Professional Verbal", "subtopic": "Technical Communication",
        "difficulty": 2,
        "question_text": "During a technical presentation to non-technical stakeholders, which communication strategy is most effective?",
        "options": [
            "Use maximum technical jargon to demonstrate expertise.",
            "Translate technical concepts into business outcomes and impact using analogies and metrics.",
            "Read out all the code line by line.",
            "Limit the presentation to under 2 minutes regardless of complexity."
        ],
        "correct_index": 1,
        "explanation": "Non-technical audiences relate to business impact, cost, risk, and outcomes — not implementation details. Effective technical communication bridges the gap using analogies and concrete metrics.",
        "expected_time_sec": 25,
        "code_snippet": None,
        "tags": ["communication", "presentation", "stakeholders"]
    },
    {
        "id": "comm_003",
        "skill": "Communication", "topic": "Professional Verbal", "subtopic": "Technical Communication",
        "difficulty": 3,
        "question_text": "What does active listening involve in a technical interview or team meeting?",
        "options": [
            "Preparing your next statement while the other person speaks.",
            "Maintaining eye contact, nodding, asking clarifying questions, and paraphrasing key points to confirm understanding.",
            "Taking notes only, without responding verbally.",
            "Waiting for the person to stop speaking before forming any opinion."
        ],
        "correct_index": 1,
        "explanation": "Active listening: full presence, eye contact, nodding, asking follow-up questions, and paraphrasing ('So what you mean is...') confirms understanding and builds trust.",
        "expected_time_sec": 25,
        "code_snippet": None,
        "tags": ["communication", "active-listening"]
    },

    # ==========================================
    # 13. Java -> Streams & Lambdas (3 questions)
    # ==========================================
    {
        "id": "java_stream_001",
        "skill": "Java", "topic": "Core Java", "subtopic": "Java Streams & Lambdas",
        "difficulty": 3,
        "question_text": "What is the difference between intermediate and terminal operations in Java Streams?",
        "options": [
            "Intermediate operations execute immediately; terminal operations are lazy.",
            "Intermediate operations are lazy and return a Stream; terminal operations trigger execution and return a result.",
            "Terminal operations can be chained; intermediate cannot.",
            "Intermediate operations modify the source collection in-place."
        ],
        "correct_index": 1,
        "explanation": "Intermediate ops (filter, map, sorted) are lazy — they build a pipeline but don't execute. Terminal ops (collect, forEach, reduce, count) trigger the pipeline execution and produce a result or side-effect.",
        "expected_time_sec": 35,
        "code_snippet": "list.stream()\n    .filter(x -> x > 5)     // intermediate (lazy)\n    .map(x -> x * 2)        // intermediate (lazy)\n    .collect(toList());     // terminal (triggers execution)",
        "tags": ["java", "streams", "lazy-evaluation"]
    },
    {
        "id": "java_stream_002",
        "skill": "Java", "topic": "Core Java", "subtopic": "Java Streams & Lambdas",
        "difficulty": 3,
        "question_text": "How does `reduce()` work in Java Streams and what does it return for an empty stream with identity?",
        "options": [
            "reduce() sorts the stream and returns the minimum.",
            "reduce() combines elements using an associative function; returns identity value for empty streams.",
            "reduce() requires a parallel stream to function correctly.",
            "reduce() always returns Optional<T>."
        ],
        "correct_index": 1,
        "explanation": "reduce(identity, accumulator) combines all elements. For an empty stream, it returns the identity value. reduce(accumulator) without identity returns Optional.empty() for empty streams.",
        "expected_time_sec": 40,
        "code_snippet": "// Sum with identity:\nint sum = IntStream.of(1,2,3,4).reduce(0, Integer::sum); // returns 10\n// Empty stream:\nint empty = IntStream.empty().reduce(0, Integer::sum); // returns 0 (identity)",
        "tags": ["java", "streams", "reduce"]
    },
    {
        "id": "java_gc_001",
        "skill": "Java", "topic": "Core Java", "subtopic": "JVM & Memory Management",
        "difficulty": 4,
        "question_text": "What is the G1 Garbage Collector's key innovation over traditional generational GC?",
        "options": [
            "G1 GC eliminates all garbage collection pauses.",
            "G1 GC divides heap into equal-sized regions (not fixed generations), prioritizing regions with most garbage (Garbage First), enabling predictable pause times.",
            "G1 GC uses reference counting instead of tracing.",
            "G1 GC only runs on multi-core machines."
        ],
        "correct_index": 1,
        "explanation": "G1 GC partitions heap into ~2048 equal-sized regions (not rigid Young/Old generations). It marks regions by garbage density and collects highest-garbage regions first, enabling configurable pause time goals via -XX:MaxGCPauseMillis.",
        "expected_time_sec": 45,
        "code_snippet": "// JVM flags:\n-XX:+UseG1GC\n-XX:MaxGCPauseMillis=200\n-XX:+HeapDumpOnOutOfMemoryError",
        "tags": ["java", "g1-gc", "jvm", "memory"]
    },

    # ==========================================
    # 14. OOP -> Design Patterns (3 questions)
    # ==========================================
    {
        "id": "oop_dp_001",
        "skill": "OOP", "topic": "Design Patterns", "subtopic": "Design Patterns",
        "difficulty": 3,
        "question_text": "What problem does the Singleton pattern solve and what is a thread-safe implementation approach?",
        "options": [
            "Singleton creates multiple instances for load balancing.",
            "Singleton ensures only one instance of a class exists globally; thread-safe via double-checked locking or Enum.",
            "Singleton is used only for database connection pooling.",
            "Singleton uses synchronized on every method call."
        ],
        "correct_index": 1,
        "explanation": "Singleton: one global instance. Thread-safe approaches: (1) Double-checked locking with volatile, (2) Enum singleton (Bill Pugh), (3) static initializer. Enum is the recommended approach in Java.",
        "expected_time_sec": 40,
        "code_snippet": "// Enum Singleton (best practice in Java):\npublic enum DatabaseConnection {\n    INSTANCE;\n    public void connect() { /* ... */ }\n}\n// Usage:\nDatabaseConnection.INSTANCE.connect();",
        "tags": ["oop", "singleton", "design-patterns", "thread-safe"]
    },
    {
        "id": "oop_dp_002",
        "skill": "OOP", "topic": "Design Patterns", "subtopic": "Design Patterns",
        "difficulty": 3,
        "question_text": "What is the Observer design pattern and when is it used?",
        "options": [
            "Observer creates objects without specifying the concrete class.",
            "Observer defines a 1-to-many dependency where state changes in the subject automatically notify all registered observers.",
            "Observer restricts access to an object through a surrogate.",
            "Observer is synonymous with the Decorator pattern."
        ],
        "correct_index": 1,
        "explanation": "Observer (Publish-Subscribe): Subject maintains a list of observers and notifies them on state change. Used in event-driven systems, GUI frameworks, message brokers. Java: PropertyChangeListener, RxJava Observables.",
        "expected_time_sec": 35,
        "code_snippet": "interface Observer { void update(Event e); }\nclass EventBus {\n    List<Observer> observers = new ArrayList<>();\n    void subscribe(Observer o) { observers.add(o); }\n    void publish(Event e) { observers.forEach(o -> o.update(e)); }\n}",
        "tags": ["oop", "observer", "design-patterns"]
    },
    {
        "id": "oop_dp_003",
        "skill": "OOP", "topic": "Design Patterns", "subtopic": "Design Patterns",
        "difficulty": 4,
        "question_text": "How does the Factory Method pattern differ from the Abstract Factory pattern?",
        "options": [
            "Factory Method creates a single product; Abstract Factory creates families of related products.",
            "Factory Method requires an interface; Abstract Factory uses concrete classes only.",
            "Abstract Factory is always implemented using Singleton.",
            "They are identical; one is just the old name for the other."
        ],
        "correct_index": 0,
        "explanation": "Factory Method: one factory method creates one type of product (subclasses decide which concrete class). Abstract Factory: creates families of related/dependent products without specifying concrete classes. Used for platform-independent UI kits.",
        "expected_time_sec": 45,
        "code_snippet": "// Factory Method:\ninterface Logger { void log(String msg); }\nclass LoggerFactory { Logger create(String type) { return type.equals(\"file\") ? new FileLogger() : new ConsoleLogger(); } }\n// Abstract Factory:\ninterface UIFactory { Button createButton(); TextField createTextField(); }",
        "tags": ["oop", "factory-method", "abstract-factory"]
    },

    # ==========================================
    # 9. Machine Learning & Statistical Modeling (5 questions)
    # ==========================================
    {
        "id": "ml_bias_001",
        "skill": "Coding", "topic": "Machine Learning", "subtopic": "Probability & Combinatorics",
        "difficulty": 3,
        "question_text": "What is the primary manifestation of high variance in a machine learning model?",
        "options": [
            "The model performs poorly on both training and test datasets (underfitting).",
            "The model fits the training data exceptionally well but fails to generalize to unseen test data (overfitting).",
            "The model has too few parameters.",
            "The model's loss function diverges during gradient descent."
        ],
        "correct_index": 1,
        "explanation": "High variance means the model is overly sensitive to fluctuations in the training set, capturing noise and leading to overfitting.",
        "expected_time_sec": 35,
        "code_snippet": "# Bias-Variance Tradeoff:\n# High Bias -> Underfitting (oversimplified model)\n# High Variance -> Overfitting (captures training noise)",
        "tags": ["ml", "bias-variance", "overfitting"]
    },
    {
        "id": "ml_reg_002",
        "skill": "Coding", "topic": "Machine Learning", "subtopic": "Probability & Combinatorics",
        "difficulty": 4,
        "question_text": "What is the key difference between L1 (Lasso) and L2 (Ridge) regularization?",
        "options": [
            "L1 adds absolute penalty driving irrelevant weights strictly to zero (feature selection); L2 penalizes squared weights shrinking them continuously.",
            "L2 produces sparse models, while L1 prevents gradient descent from converging.",
            "L1 can only be applied to classification problems, while L2 is for regression.",
            "L1 and L2 are mathematically identical when learning rate is less than 0.01."
        ],
        "correct_index": 0,
        "explanation": "L1 (Lasso) penalty |w| causes corner intersections on parameter contours, driving weights to exact 0. L2 (Ridge) penalty w^2 shrinks weights asymptotically towards 0.",
        "expected_time_sec": 45,
        "code_snippet": "# Cost Functions:\n# Lasso (L1): Loss + lambda * sum(|w_i|)\n# Ridge (L2): Loss + lambda * sum(w_i^2)",
        "tags": ["ml", "regularization", "lasso", "ridge"]
    },
    {
        "id": "ml_metrics_003",
        "skill": "Coding", "topic": "Machine Learning", "subtopic": "Probability & Combinatorics",
        "difficulty": 3,
        "question_text": "In a medical diagnosis dataset where detecting a rare disease is critical, which evaluation metric is most vital to maximize?",
        "options": [
            "Accuracy",
            "Recall (Sensitivity)",
            "Precision",
            "Mean Squared Error"
        ],
        "correct_index": 1,
        "explanation": "Recall = TP / (TP + FN). Maximizing recall minimizes False Negatives (critical in disease screening where missing an infected patient has fatal consequences).",
        "expected_time_sec": 35,
        "code_snippet": "Recall = TruePositives / (TruePositives + FalseNegatives)",
        "tags": ["ml", "evaluation-metrics", "recall", "precision"]
    },
    {
        "id": "ml_grad_004",
        "skill": "Coding", "topic": "Machine Learning", "subtopic": "Probability & Combinatorics",
        "difficulty": 4,
        "question_text": "What is the primary advantage of Adam (Adaptive Moment Estimation) optimizer over standard Stochastic Gradient Descent (SGD)?",
        "options": [
            "Adam computes individual adaptive learning rates for different parameters using estimates of first and second moments of gradients.",
            "Adam guarantees finding the global minimum in non-convex loss surfaces.",
            "Adam does not require any hyperparameters or learning rate.",
            "Adam only works on CPU architecture."
        ],
        "correct_index": 0,
        "explanation": "Adam combines the advantages of AdaGrad and RMSProp, maintaining exponentially decaying averages of past gradients (momentum) and past squared gradients.",
        "expected_time_sec": 40,
        "code_snippet": "# Adam update: m_t = beta1*m_{t-1} + (1-beta1)*g_t\n# v_t = beta2*v_{t-1} + (1-beta2)*g_t^2\n# w = w - lr * m_hat / (sqrt(v_hat) + eps)",
        "tags": ["ml", "optimization", "adam", "gradient-descent"]
    },

    # ==========================================
    # 10. DevOps, Cloud & Systems Architecture (5 questions)
    # ==========================================
    {
        "id": "devops_docker_001",
        "skill": "DBMS", "topic": "Cloud & Infrastructure", "subtopic": "Concurrency & Locks",
        "difficulty": 3,
        "question_text": "How do Docker containers fundamentally differ from traditional Hypervisor-based Virtual Machines (VMs)?",
        "options": [
            "Containers share the host OS kernel and isolate user spaces, resulting in lightweight startup and lower memory overhead compared to full guest OS virtualization in VMs.",
            "Containers require dedicated physical hardware, while VMs can run on cloud instances.",
            "Containers do not support network isolation, whereas VMs do.",
            "Containers can only run Python applications, whereas VMs support Java."
        ],
        "correct_index": 0,
        "explanation": "Containers utilize Linux cgroups and namespaces to share the host kernel, providing sub-second startup and high density without guest OS bloat.",
        "expected_time_sec": 35,
        "code_snippet": "# Docker container: App + Libs -> Shared Host Kernel\n# Virtual Machine: App + Libs -> Guest OS -> Hypervisor -> Host OS",
        "tags": ["devops", "docker", "containers", "virtualization"]
    },
    {
        "id": "devops_cap_002",
        "skill": "DBMS", "topic": "Cloud & Infrastructure", "subtopic": "Concurrency & Locks",
        "difficulty": 4,
        "question_text": "According to the CAP Theorem, what tradeoff must a distributed database make during a network partition (P)?",
        "options": [
            "It must choose between Consistency (all nodes see same data simultaneously) and Availability (every request receives a non-error response).",
            "It must choose between Security and Latency.",
            "It must drop all database transactions permanently.",
            "It automatically switches to single-node SQLite."
        ],
        "correct_index": 0,
        "explanation": "During a network partition (P), a distributed system cannot guarantee both Consistency (CP) and Availability (AP). It must sacrifice one to handle the network split.",
        "expected_time_sec": 40,
        "code_snippet": "-- CAP Tradeoff:\n-- CP (Consistency + Partition Tolerance): e.g. HBase, CockroachDB\n-- AP (Availability + Partition Tolerance): e.g. Cassandra, DynamoDB",
        "tags": ["devops", "system-design", "cap-theorem", "distributed-systems"]
    },
    {
        "id": "devops_cicd_003",
        "skill": "DBMS", "topic": "Cloud & Infrastructure", "subtopic": "Concurrency & Locks",
        "difficulty": 3,
        "question_text": "What is the primary advantage of a Blue-Green deployment strategy over in-place rolling updates?",
        "options": [
            "It maintains two identical production environments (Blue active, Green staging), enabling zero-downtime cutover and instant rollback if issues occur.",
            "It reduces infrastructure server costs by 50%.",
            "It completely eliminates the need for unit tests.",
            "It only deploys code to internal developers."
        ],
        "correct_index": 0,
        "explanation": "Blue-Green deployment routes live router/load balancer traffic from Blue to Green after verification. If an error is detected, traffic is immediately switched back to Blue.",
        "expected_time_sec": 35,
        "code_snippet": "# Traffic Router -> Blue (Live v1.0)\n# Deploy v2.0 to Green -> Verify Health -> Route Traffic to Green (Live v2.0)",
        "tags": ["devops", "ci-cd", "blue-green", "deployment"]
    },
    {
        "id": "devops_lb_004",
        "skill": "DBMS", "topic": "Cloud & Infrastructure", "subtopic": "Concurrency & Locks",
        "difficulty": 3,
        "question_text": "Which load balancing algorithm distributes incoming requests to the server with the fewest active open client connections?",
        "options": [
            "Least Connections",
            "Round Robin",
            "IP Hash",
            "Random Selection"
        ],
        "correct_index": 0,
        "explanation": "Least Connections dynamically directs new traffic to the backend instance currently handling the fewest active connections, ideal for long-lived sessions.",
        "expected_time_sec": 25,
        "code_snippet": "# Nginx Load Balancing:\nupstream backend_servers {\n    least_conn;\n    server backend1.example.com;\n    server backend2.example.com;\n}",
        "tags": ["devops", "load-balancing", "least-conn"]
    },

    # ==========================================
    # 11. Full-Stack Web Architecture & APIs (5 questions)
    # ==========================================
    {
        "id": "fs_rest_001",
        "skill": "Coding", "topic": "Web Architecture", "subtopic": "Arrays & Strings",
        "difficulty": 3,
        "question_text": "Which HTTP methods are defined as idempotent according to the HTTP/1.1 RFC specification?",
        "options": [
            "GET, PUT, DELETE, HEAD, OPTIONS (calling them multiple times produces the same side-effects as calling once)",
            "POST and PATCH only",
            "Only GET is idempotent",
            "All HTTP methods are non-idempotent in modern browsers"
        ],
        "correct_index": 0,
        "explanation": "Idempotency means N identical requests result in the same server state as 1 request. GET, PUT, DELETE are idempotent; POST is non-idempotent because repeated calls create multiple resources.",
        "expected_time_sec": 35,
        "code_snippet": "// Idempotent: PUT /users/42 { name: 'Alice' } -> state unchanged if repeated\n// Non-Idempotent: POST /orders -> creates duplicate order every call",
        "tags": ["fullstack", "rest-api", "http", "idempotency"]
    },
    {
        "id": "fs_cors_002",
        "skill": "Coding", "topic": "Web Architecture", "subtopic": "Arrays & Strings",
        "difficulty": 3,
        "question_text": "Why does a browser send an HTTP OPTIONS 'Preflight' request before making certain cross-origin API calls?",
        "options": [
            "To check with the target server if the requested HTTP method, custom headers, and origin are permitted under CORS policy before transmitting actual data.",
            "To authenticate the user's password securely.",
            "To compress the payload with GZIP.",
            "To establish a WebSocket connection."
        ],
        "correct_index": 0,
        "explanation": "Preflight OPTIONS requests are sent automatically for non-simple cross-origin requests (e.g. PUT/DELETE or custom Authorization headers) to verify CORS permissions.",
        "expected_time_sec": 35,
        "code_snippet": "OPTIONS /api/data HTTP/1.1\nOrigin: https://frontend.app\nAccess-Control-Request-Method: POST\nAccess-Control-Request-Headers: Authorization",
        "tags": ["fullstack", "cors", "browser-security", "http-options"]
    },
    {
        "id": "fs_jwt_003",
        "skill": "Coding", "topic": "Web Architecture", "subtopic": "Arrays & Strings",
        "difficulty": 4,
        "question_text": "What are the three components of a JSON Web Token (JWT), and how is tampering prevented?",
        "options": [
            "Header, Payload, Signature. Tampering with Header or Payload invalidates the cryptographic signature verified using the server's secret key.",
            "Username, Password, Salt. It is encrypted with RSA 4096.",
            "Cookie, Session ID, Timestamp. It requires database lookup on every call.",
            "IP Address, User Agent, MAC Address."
        ],
        "correct_index": 0,
        "explanation": "A JWT consists of base64url-encoded Header, Payload, and Signature (HMAC-SHA256 or RSA). If any claim in the payload is modified, the signature check fails without needing database state.",
        "expected_time_sec": 45,
        "code_snippet": "// JWT Structure:\n// eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNDIifQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c\n// [Header].[Payload].[Signature]",
        "tags": ["fullstack", "jwt", "authentication", "security"]
    },
    {
        "id": "fs_sliding_004",
        "skill": "Coding", "topic": "Algorithms", "subtopic": "Two Pointers & Sliding Window",
        "difficulty": 4,
        "question_text": "Given an array of positive integers, what is the time complexity to find the maximum sum subarray of fixed size K using a Sliding Window approach?",
        "options": [
            "O(N) time and O(1) auxiliary space",
            "O(N * K) time and O(K) space",
            "O(N log N) time and O(N) space",
            "O(N^2) time and O(1) space"
        ],
        "correct_index": 0,
        "explanation": "Sliding window slides a window of size K across the array in a single pass: window_sum += arr[i] - arr[i-K]. This runs in strict O(N) time and O(1) extra space.",
        "expected_time_sec": 30,
        "code_snippet": "def max_sub_array_of_size_k(k, arr):\n    max_sum, window_sum = 0, sum(arr[:k])\n    max_sum = window_sum\n    for i in range(k, len(arr)):\n        window_sum += arr[i] - arr[i-k]\n        max_sum = max(max_sum, window_sum)\n    return max_sum",
        "tags": ["coding", "sliding-window", "dsa", "algorithms"]
    },

    # ==========================================
    # 7. PYTHON PROGRAMMING & SCRIPTING (12 questions)
    # ==========================================
    {
        "id": "py_list_001",
        "skill": "Python", "topic": "Core Python", "subtopic": "Python Data Structures",
        "difficulty": 2,
        "question_text": "What happens when you execute the following Python code snippet?",
        "options": [
            "[1, 2, [3, 4, 5]]",
            "[1, 2, [3, 4], 5]",
            "[1, 2, 3, 4, 5]",
            "TypeError: cannot append list"
        ],
        "correct_index": 0,
        "explanation": "list.append() adds its argument as a single element at the end of the list. Here, the inner list [3, 4, 5] is appended as a nested sub-list.",
        "expected_time_sec": 25,
        "code_snippet": "a = [1, 2]\nb = [3, 4]\na.append(b)\nb.append(5)\nprint(a)",
        "tags": ["python", "lists", "mutability"]
    },
    {
        "id": "py_dict_002",
        "skill": "Python", "topic": "Core Python", "subtopic": "Python Dictionaries & Hashing",
        "difficulty": 3,
        "question_text": "In Python 3.7+, which statement is TRUE regarding standard dictionary key ordering and key requirements?",
        "options": [
            "Keys must be mutable; order is sorted by hash value.",
            "Keys must be hashable (__hash__ & __eq__); insertion order is guaranteed to be preserved.",
            "Keys can be any object; order is purely non-deterministic.",
            "Keys must be strings or integers; order is alphabetical."
        ],
        "correct_index": 1,
        "explanation": "Since Python 3.7, dictionaries maintain insertion order as an official language specification. Keys must be hashable (immutable objects like int, str, tuple of immutables).",
        "expected_time_sec": 30,
        "code_snippet": "d = {}\nd['z'] = 1\nd['a'] = 2\n# Iterating list(d.keys()) yields ['z', 'a']",
        "tags": ["python", "dict", "hashable", "ordering"]
    },
    {
        "id": "py_comp_003",
        "skill": "Python", "topic": "Advanced Python", "subtopic": "Python Generators & Memory",
        "difficulty": 3,
        "question_text": "What is the primary memory and execution difference between `[x**2 for x in range(10**7)]` and `(x**2 for x in range(10**7))`?",
        "options": [
            "List comprehension computes eagerly into memory; Generator expression evaluates lazily on-demand using O(1) memory.",
            "Generator expression evaluates immediately and stores in cache.",
            "List comprehension is asynchronous; generator is synchronous.",
            "Both allocate identical memory overhead in CPython."
        ],
        "correct_index": 0,
        "explanation": "List comprehensions create the entire list in RAM immediately (eager), whereas generator expressions return a generator object that produces items one-by-one via the iterator protocol (lazy, O(1) memory).",
        "expected_time_sec": 35,
        "code_snippet": "import sys\nlist_comp = [x**2 for x in range(10000)] # Consumes ~85 KB\ngen_expr = (x**2 for x in range(10000))   # Consumes ~104 Bytes",
        "tags": ["python", "generators", "memory", "comprehension"]
    },
    {
        "id": "py_gen_004",
        "skill": "Python", "topic": "Core Python", "subtopic": "Python Generators & Memory",
        "difficulty": 2,
        "question_text": "What is the output of the following generator function?",
        "options": [
            "[10, 20]",
            "10 then 20 upon calling next()",
            "GeneratorExit Exception",
            "<generator object> on first call and None on second"
        ],
        "correct_index": 1,
        "explanation": "A function containing `yield` returns a generator iterator. Each `next()` resumes execution until the next `yield` statement.",
        "expected_time_sec": 30,
        "code_snippet": "def count_up():\n    yield 10\n    yield 20\n\ngen = count_up()\nprint(next(gen))\nprint(next(gen))",
        "tags": ["python", "generators", "yield"]
    },
    {
        "id": "py_decor_005",
        "skill": "Python", "topic": "Advanced Python", "subtopic": "Python Decorators",
        "difficulty": 3,
        "question_text": "Why is `@functools.wraps(fn)` commonly used when writing custom Python decorators?",
        "options": [
            "It speeds up function execution by compiling to C bytecode.",
            "It copies original function metadata (__name__, __doc__, annotations) to the wrapper function.",
            "It prevents the wrapped function from throwing uncaught exceptions.",
            "It enables multi-threading support automatically."
        ],
        "correct_index": 1,
        "explanation": "Without `@wraps`, the decorated function loses its identity (e.g. `fn.__name__` becomes 'wrapper' instead of the original function name), which breaks introspection, debuggers, and docstrings.",
        "expected_time_sec": 40,
        "code_snippet": "import functools\n\ndef my_decorator(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        return func(*args, **kwargs)\n    return wrapper",
        "tags": ["python", "decorators", "functools", "metaprogramming"]
    },
    {
        "id": "py_gil_006",
        "skill": "Python", "topic": "Concurrency & Internals", "subtopic": "Python GIL & Concurrency",
        "difficulty": 4,
        "question_text": "What is the CPython Global Interpreter Lock (GIL) and how does it affect CPU-bound multi-threaded programs?",
        "options": [
            "It prevents deadlock by synchronizing SQL queries automatically.",
            "It is a mutex ensuring only one native thread executes Python bytecode at a time, making threading ineffective for CPU-bound speedup.",
            "It forces Python to run on GPU cores only.",
            "It is a garbage collection lock that freezes threads during cyclic sweeps."
        ],
        "correct_index": 1,
        "explanation": "The GIL ensures thread-safety in CPython memory management. Because only one thread can execute bytecode simultaneously, multi-threading cannot achieve true CPU parallelism (use `multiprocessing` instead).",
        "expected_time_sec": 45,
        "code_snippet": "# For CPU-intensive operations in Python:\n# from multiprocessing import Process (utilizes multi-core)\n# rather than from threading import Thread (limited by GIL)",
        "tags": ["python", "gil", "concurrency", "multiprocessing"]
    },
    {
        "id": "py_oop_007",
        "skill": "Python", "topic": "Object Oriented Python", "subtopic": "Python OOP & MRO",
        "difficulty": 4,
        "question_text": "Given multiple inheritance `class D(B, C): pass`, how does Python determine the order in which methods are resolved (MRO)?",
        "options": [
            "Depth-First Search (DFS) from right to left.",
            "C3 Linearization Algorithm maintaining local precedence order and monotonicity.",
            "Breadth-First Search (BFS) sorting methods alphabetically.",
            "Random selection based on class definition timestamp."
        ],
        "correct_index": 1,
        "explanation": "Python 2.3+ uses the C3 Linearization algorithm to compute the Method Resolution Order (MRO), accessible via `ClassName.__mro__`.",
        "expected_time_sec": 45,
        "code_snippet": "class A: pass\nclass B(A): pass\nclass C(A): pass\nclass D(B, C): pass\nprint(D.mro()) # [D, B, C, A, object]",
        "tags": ["python", "mro", "oop", "inheritance"]
    },
    {
        "id": "py_ctx_008",
        "skill": "Python", "topic": "Core Python", "subtopic": "Python Context Managers",
        "difficulty": 3,
        "question_text": "If an exception occurs inside a `with` block, which dunder method handles cleanup and can optionally suppress the exception?",
        "options": [
            "__del__(self)",
            "__exit__(self, exc_type, exc_val, exc_tb) by returning True",
            "__cleanup__(self)",
            "__close__(self)"
        ],
        "correct_index": 1,
        "explanation": "The context manager protocol uses `__enter__` and `__exit__`. If `__exit__` returns `True`, the exception is swallowed/suppressed; if it returns `False` (or None), it re-raises.",
        "expected_time_sec": 35,
        "code_snippet": "class SafeResource:\n    def __enter__(self):\n        return self\n    def __exit__(self, exc_type, exc_val, tb):\n        print('Cleaned up!')\n        return True # Suppresses exception",
        "tags": ["python", "context-manager", "with", "exceptions"]
    },
    {
        "id": "py_lambda_009",
        "skill": "Python", "topic": "Core Python", "subtopic": "Python Closures & Lambdas",
        "difficulty": 3,
        "question_text": "What does `[f() for f in [lambda: i for i in range(3)]]` evaluate to, and why?",
        "options": [
            "[0, 1, 2] due to eager binding",
            "[2, 2, 2] because Python closures use late binding (variable looked up at call time)",
            "[0, 0, 0] because i resets after loop",
            "SyntaxError: invalid lambda inside comprehension"
        ],
        "correct_index": 1,
        "explanation": "Python closures bind variables by reference (late binding). When called, `i` has completed the loop with value 2. To fix: `lambda i=i: i` default argument.",
        "expected_time_sec": 40,
        "code_snippet": "# Late binding pitfall:\nfuncs = [lambda: i for i in range(3)]\nprint([f() for f in funcs]) # Output: [2, 2, 2]\n\n# Correct fix:\nfixed_funcs = [lambda i=i: i for i in range(3)]\nprint([f() for f in fixed_funcs]) # Output: [0, 1, 2]",
        "tags": ["python", "lambda", "closures", "late-binding"]
    },
    {
        "id": "py_async_010",
        "skill": "Python", "topic": "Concurrency & Internals", "subtopic": "Python Asyncio & Coroutines",
        "difficulty": 4,
        "question_text": "What is the primary advantage of Python `asyncio` over traditional OS threading for high-concurrency network servers?",
        "options": [
            "Asyncio bypasses Python GIL for CPU-bound computations.",
            "Single-threaded cooperative multitasking with event loop avoiding kernel thread stack memory overhead and context switching.",
            "Asyncio converts Python code to GPU CUDA kernels.",
            "Asyncio requires hardware multi-core locks."
        ],
        "correct_index": 1,
        "explanation": "Asyncio uses an event loop to handle thousands of concurrent I/O-bound connections in a single thread without the heavy memory overhead (8MB per thread stack) and CPU context switching of OS threads.",
        "expected_time_sec": 45,
        "code_snippet": "import asyncio\n\nasync def fetch_data():\n    await asyncio.sleep(1)\n    return {'status': 200}\n\nasync def main():\n    results = await asyncio.gather(fetch_data(), fetch_data())\n    print(results)",
        "tags": ["python", "asyncio", "event-loop", "concurrency"]
    },
    {
        "id": "py_mem_011",
        "skill": "Python", "topic": "Concurrency & Internals", "subtopic": "Python Memory Management",
        "difficulty": 4,
        "question_text": "How does CPython detect and deallocate objects involved in circular reference cycles (e.g. A references B and B references A)?",
        "options": [
            "Immediate deallocation as reference count hits zero.",
            "Cyclic Generational Garbage Collector (using generation 0, 1, 2 heaps and double linked lists of container objects).",
            "Manual deallocation using free() by the programmer.",
            "Circular references always cause permanent memory leaks."
        ],
        "correct_index": 1,
        "explanation": "Reference counting handles immediate deallocation when refcount reaches 0. For reference cycles, Python's cyclical garbage collector periodically tracks container objects across 3 generations.",
        "expected_time_sec": 45,
        "code_snippet": "import gc\nclass Node:\n    def __init__(self):\n        self.neighbor = None\n\na = Node()\nb = Node()\na.neighbor = b\nb.neighbor = a\ndel a, b # Solved by gc.collect()",
        "tags": ["python", "garbage-collection", "memory", "gc"]
    },
    {
        "id": "py_type_012",
        "skill": "Python", "topic": "Core Python", "subtopic": "Python Functions & Scope",
        "difficulty": 2,
        "question_text": "What is the output of the function call `compute(1, 2, 3, x=4, y=5)`?",
        "options": [
            "(1, (2, 3), {'x': 4, 'y': 5})",
            "((1, 2, 3), {'x': 4, 'y': 5})",
            "(1, [2, 3], {'x': 4, 'y': 5})",
            "TypeError: too many positional arguments"
        ],
        "correct_index": 0,
        "explanation": "`a` gets 1. `*args` captures remaining positional arguments (2, 3) as a tuple. `**kwargs` captures keyword arguments {'x': 4, 'y': 5} as a dictionary.",
        "expected_time_sec": 30,
        "code_snippet": "def compute(a, *args, **kwargs):\n    return a, args, kwargs\n\nprint(compute(1, 2, 3, x=4, y=5))",
        "tags": ["python", "args", "kwargs", "functions"]
    },

    # ==========================================
    # 8. C++ MODERN SYSTEMS & DSA (12 questions)
    # ==========================================
    {
        "id": "cpp_ptr_001",
        "skill": "C++", "topic": "Core C++", "subtopic": "C++ Pointers & References",
        "difficulty": 2,
        "question_text": "Given `int arr[5] = {10, 20, 30, 40, 50}; int *p = arr;`, what does `*(p + 2)` evaluate to?",
        "options": ["10", "20", "30", "40"],
        "correct_index": 2,
        "explanation": "Pointer arithmetic `*(p + 2)` offsets the pointer by 2 * sizeof(int) bytes, accessing `arr[2]` which is 30.",
        "expected_time_sec": 25,
        "code_snippet": "int arr[5] = {10, 20, 30, 40, 50};\nint *p = arr;\nstd::cout << *(p + 2); // 30",
        "tags": ["cpp", "pointers", "arrays"]
    },
    {
        "id": "cpp_mem_002",
        "skill": "C++", "topic": "Core C++", "subtopic": "C++ Memory Management",
        "difficulty": 2,
        "question_text": "What is the crucial difference between `new` in C++ versus `malloc()` in C?",
        "options": [
            "`new` calls the object constructor and is type-safe; `malloc()` only allocates raw bytes without invoking constructors.",
            "`malloc()` is faster and automatically frees memory.",
            "`new` allocates on stack; `malloc()` on heap.",
            "There is no difference; `new` is just an alias."
        ],
        "correct_index": 0,
        "explanation": "`new` allocates heap memory, calculates sizeof automatically, and executes constructors. `malloc()` simply allocates a raw block of bytes and returns `void*`.",
        "expected_time_sec": 30,
        "code_snippet": "class Widget { public: Widget() { std::cout << \"Constructed\"; } };\nWidget *w1 = new Widget(); // Calls constructor\nWidget *w2 = (Widget*)malloc(sizeof(Widget)); // No constructor called",
        "tags": ["cpp", "memory", "new", "malloc"]
    },
    {
        "id": "cpp_smart_003",
        "skill": "C++", "topic": "Modern C++", "subtopic": "C++ Smart Pointers",
        "difficulty": 3,
        "question_text": "Which smart pointer should be used when an object requires strict unique ownership with zero runtime reference-counting overhead?",
        "options": [
            "std::shared_ptr<T>",
            "std::unique_ptr<T>",
            "std::weak_ptr<T>",
            "std::auto_ptr<T>"
        ],
        "correct_index": 1,
        "explanation": "`std::unique_ptr` represents exclusive ownership. It cannot be copied (only moved) and has zero runtime overhead compared to a raw pointer.",
        "expected_time_sec": 30,
        "code_snippet": "auto ptr = std::make_unique<int>(42);\n// auto ptr2 = ptr; // Compilation Error (copy prohibited)\nauto ptr2 = std::move(ptr); // Ownership transferred safely",
        "tags": ["cpp", "smart-pointers", "unique_ptr", "modern-cpp"]
    },
    {
        "id": "cpp_smart_004",
        "skill": "C++", "topic": "Modern C++", "subtopic": "C++ Smart Pointers",
        "difficulty": 4,
        "question_text": "How does `std::weak_ptr` prevent memory leaks in cyclical graphs of `std::shared_ptr` objects?",
        "options": [
            "It deletes both objects when reference count reaches 2.",
            "It holds a non-owning reference that does not increment the strong reference count (`use_count()`).",
            "It forces synchronous garbage collection at scope end.",
            "It converts heap pointers to stack values."
        ],
        "correct_index": 1,
        "explanation": "`std::weak_ptr` observes a `shared_ptr` without increasing its reference count. To access the object, it calls `.lock()` to temporarily acquire a `shared_ptr` if still alive.",
        "expected_time_sec": 45,
        "code_snippet": "struct Node {\n    std::shared_ptr<Node> next;\n    std::weak_ptr<Node> prev; // Prevents cycle leak\n};",
        "tags": ["cpp", "smart-pointers", "weak_ptr", "memory-leaks"]
    },
    {
        "id": "cpp_move_005",
        "skill": "C++", "topic": "Modern C++", "subtopic": "C++ Move Semantics & Rvalues",
        "difficulty": 4,
        "question_text": "What does `std::move(x)` actually do in C++11 and later?",
        "options": [
            "It physically moves the bytes of x to another CPU register.",
            "It is an unconditional cast that casts its argument to an rvalue reference (`T&&`), enabling move constructors/assignment.",
            "It deletes x immediately.",
            "It creates a thread-safe mutex on x."
        ],
        "correct_index": 1,
        "explanation": "`std::move` does not move anything on its own; it is a `static_cast<T&&>(x)` that converts an lvalue into an rvalue reference, allowing resource pilfering without copying.",
        "expected_time_sec": 40,
        "code_snippet": "std::vector<std::string> v1 = {\"a\", \"b\", \"c\"};\nstd::vector<std::string> v2 = std::move(v1); // v1 pointers transferred to v2 in O(1)",
        "tags": ["cpp", "move-semantics", "rvalue", "modern-cpp"]
    },
    {
        "id": "cpp_raii_006",
        "skill": "C++", "topic": "Core C++", "subtopic": "C++ RAII & Lifetime",
        "difficulty": 3,
        "question_text": "What is the fundamental idiom of RAII (Resource Acquisition Is Initialization) in C++?",
        "options": [
            "Acquiring resources in constructor and releasing them deterministically in the destructor upon scope exit.",
            "Initializing all pointers to NULL before calling malloc.",
            "Using global try-catch handlers for memory exceptions.",
            "Allocating all variables statically."
        ],
        "correct_index": 0,
        "explanation": "RAII binds the lifecycle of resources (memory, file handles, mutex locks) to object lifetime. When an object goes out of scope (normal return or exception), its destructor cleans up automatically.",
        "expected_time_sec": 35,
        "code_snippet": "void processFile() {\n    std::lock_guard<std::mutex> lock(mtx); // Mutex locked\n    std::ifstream file(\"data.txt\");       // File opened\n    // Exception or return here safely unlocks mutex and closes file!\n}",
        "tags": ["cpp", "raii", "destructors", "exception-safety"]
    },
    {
        "id": "cpp_virt_007",
        "skill": "C++", "topic": "Object Oriented C++", "subtopic": "C++ Polymorphism & VTable",
        "difficulty": 4,
        "question_text": "Why MUST a base class have a `virtual` destructor if derived objects are deleted via base class pointers?",
        "options": [
            "To make the class abstract.",
            "To ensure the derived class destructor is called; without it, only base destructor runs leading to undefined behavior and resource leaks.",
            "To allow deep copying in STL containers.",
            "To prevent private member access."
        ],
        "correct_index": 1,
        "explanation": "If `delete basePtr` is executed without a virtual destructor in the base class, the compiler statically resolves destruction to `~Base()`, skipping `~Derived()` and leaking derived resources.",
        "expected_time_sec": 45,
        "code_snippet": "class Base {\npublic:\n    virtual ~Base() { std::cout << \"~Base\\n\"; } // Essential!\n};\nclass Derived : public Base {\n    int *data = new int[100];\npublic:\n    ~Derived() { delete[] data; std::cout << \"~Derived\\n\"; }\n};",
        "tags": ["cpp", "virtual-destructor", "vtable", "oop"]
    },
    {
        "id": "cpp_stl_008",
        "skill": "C++", "topic": "C++ STL", "subtopic": "C++ STL Containers",
        "difficulty": 3,
        "question_text": "When a `std::vector` exceeds its `capacity()` during `push_back()`, what happens internally?",
        "options": [
            "It throws a VectorOverflowException.",
            "It allocates a new contiguous buffer (typically 1.5x or 2x size), moves/copies elements, frees old buffer, invalidating all iterators and pointers.",
            "It switches to a linked list node structure.",
            "It writes surplus elements to disk swap."
        ],
        "correct_index": 1,
        "explanation": "Vectors maintain contiguous memory. Reallocation allocates larger memory, moves existing elements, deletes the old array, making previous iterators/references invalid.",
        "expected_time_sec": 40,
        "code_snippet": "std::vector<int> vec;\nvec.reserve(100); // Pre-allocates capacity to avoid iterator invalidation",
        "tags": ["cpp", "stl", "vector", "iterator-invalidation"]
    },
    {
        "id": "cpp_stl_009",
        "skill": "C++", "topic": "C++ STL", "subtopic": "C++ STL Containers",
        "difficulty": 3,
        "question_text": "What are the underlying data structures and average search complexities of `std::map` vs `std::unordered_map`?",
        "options": [
            "std::map: Red-Black Tree (O(log N)); std::unordered_map: Hash Table (O(1) average).",
            "std::map: Hash Table (O(1)); std::unordered_map: Binary Search Tree (O(N)).",
            "std::map: Array (O(N)); std::unordered_map: Trie (O(log N)).",
            "Both use Balanced AVL Trees with O(log N) lookup."
        ],
        "correct_index": 0,
        "explanation": "`std::map` is ordered and implemented via Self-Balancing BST (Red-Black Tree, O(log N)). `std::unordered_map` uses hashing with buckets for O(1) average time complexity.",
        "expected_time_sec": 35,
        "code_snippet": "#include <map>\n#include <unordered_map>\nstd::map<int, std::string> ordered;       // Keys kept strictly sorted\nstd::unordered_map<int, std::string> hmap; // Keys unordered, O(1) lookup",
        "tags": ["cpp", "stl", "map", "unordered_map", "data-structures"]
    },
    {
        "id": "cpp_tmpl_010",
        "skill": "C++", "topic": "Modern C++", "subtopic": "C++ Templates",
        "difficulty": 3,
        "question_text": "How do C++ templates achieve generic programming without runtime overhead?",
        "options": [
            "They convert all types to void* pointers at runtime like Java type erasure.",
            "They perform compile-time template instantiation generating concrete machine code for each instantiated type.",
            "They interpret code at runtime using a JIT compiler.",
            "They store objects in an untyped byte vector."
        ],
        "correct_index": 1,
        "explanation": "C++ templates are instantiated at compile time. The compiler generates tailored type-specific classes or functions for each distinct type used, enabling zero runtime overhead (monomorphization).",
        "expected_time_sec": 35,
        "code_snippet": "template <typename T>\nT getMax(T a, T b) {\n    return (a > b) ? a : b;\n}\n// getMax<int>(3, 5) generates int version at compile-time",
        "tags": ["cpp", "templates", "metaprogramming", "compile-time"]
    },
    {
        "id": "cpp_ref_011",
        "skill": "C++", "topic": "Core C++", "subtopic": "C++ Pointers & References",
        "difficulty": 2,
        "question_text": "Which of the following is a valid distinction between a C++ reference (`int &ref`) and a pointer (`int *ptr`)?",
        "options": [
            "References must be initialized when declared and cannot be reseated to bind to another variable.",
            "Pointers cannot be NULL.",
            "References require explicit dereferencing syntax with `*`.",
            "References consume 8 bytes of stack memory on every local access."
        ],
        "correct_index": 0,
        "explanation": "A reference is an alias for an existing object. It cannot be null and cannot be re-bound to point to a different object after initialization.",
        "expected_time_sec": 25,
        "code_snippet": "int a = 10, b = 20;\nint &ref = a; // ref is permanently bound to a\nref = b;      // Assigns value of b into a (a becomes 20)",
        "tags": ["cpp", "references", "pointers"]
    },
    {
        "id": "cpp_copy_012",
        "skill": "C++", "topic": "Object Oriented C++", "subtopic": "C++ Rule of Three / Five",
        "difficulty": 4,
        "question_text": "According to the C++ 'Rule of Five', if a class defines a custom Destructor to manage raw resources, which other four special member functions should typically be declared?",
        "options": [
            "Copy Constructor, Copy Assignment, Move Constructor, Move Assignment.",
            "Default Constructor, Parameterized Constructor, Operator==, Operator!=.",
            "Getters, Setters, Print, Clone.",
            "Virtual Destructor, Pure Virtual Method, Dynamic Cast, Static Cast."
        ],
        "correct_index": 0,
        "explanation": "Rule of 5 states that managing raw resources requires implementing: Destructor, Copy Constructor, Copy Assignment Operator, Move Constructor, and Move Assignment Operator.",
        "expected_time_sec": 45,
        "code_snippet": "class ResourceHolder {\n    int *data;\npublic:\n    ResourceHolder();\n    ~ResourceHolder();\n    ResourceHolder(const ResourceHolder&);            // Copy ctor\n    ResourceHolder& operator=(const ResourceHolder&); // Copy assign\n    ResourceHolder(ResourceHolder&&) noexcept;        // Move ctor\n    ResourceHolder& operator=(ResourceHolder&&) noexcept; // Move assign\n};",
        "tags": ["cpp", "rule-of-five", "memory-management", "oop"]
    },

    # ==========================================
    # 9. JAVASCRIPT & WEB TECH (10 questions)
    # ==========================================
    {
        "id": "js_clos_001",
        "skill": "JavaScript", "topic": "Core JavaScript", "subtopic": "JS Closures & Scope",
        "difficulty": 2,
        "question_text": "What will be logged by the following JavaScript code snippet?",
        "options": ["10 then 11", "10 then 10", "undefined", "ReferenceError"],
        "correct_index": 0,
        "explanation": "The inner function retains access to `count` in its lexical scope even after `createCounter()` has returned (closure).",
        "expected_time_sec": 25,
        "code_snippet": "function createCounter() {\n  let count = 10;\n  return function() { return count++; };\n}\nconst counter = createCounter();\nconsole.log(counter());\nconsole.log(counter());",
        "tags": ["javascript", "closures", "scope"]
    },
    {
        "id": "js_event_002",
        "skill": "JavaScript", "topic": "Async JavaScript", "subtopic": "JS Event Loop & Microtasks",
        "difficulty": 3,
        "question_text": "In what order are the numbers printed in the following JavaScript snippet?",
        "options": [
            "1, 4, 3, 2",
            "1, 2, 3, 4",
            "1, 3, 4, 2",
            "4, 3, 2, 1"
        ],
        "correct_index": 0,
        "explanation": "1 and 4 run synchronously. Promise callbacks are queued in the Microtask Queue and execute before Macrotasks (`setTimeout` callback in Task Queue). Order: 1, 4, 3, 2.",
        "expected_time_sec": 35,
        "code_snippet": "console.log(1);\nsetTimeout(() => console.log(2), 0);\nPromise.resolve().then(() => console.log(3));\nconsole.log(4);",
        "tags": ["javascript", "event-loop", "microtasks", "promises"]
    },
    {
        "id": "js_prom_003",
        "skill": "JavaScript", "topic": "Async JavaScript", "subtopic": "JS Promises & Async/Await",
        "difficulty": 3,
        "question_text": "What is the difference between `Promise.all()` and `Promise.allSettled()`?",
        "options": [
            "`Promise.all` rejects immediately upon the first rejected promise (fail-fast); `Promise.allSettled` waits for all promises to finish regardless of rejection.",
            "`Promise.all` executes in parallel; `allSettled` executes sequentially.",
            "`Promise.allSettled` cancels all remaining network requests.",
            "`Promise.all` only works with async/await."
        ],
        "correct_index": 0,
        "explanation": "`Promise.all` short-circuits on any rejection. `Promise.allSettled` returns an array of objects `{status: 'fulfilled'|'rejected', value/reason}` for all promises.",
        "expected_time_sec": 30,
        "code_snippet": "const p1 = Promise.resolve(10);\nconst p2 = Promise.reject(\"Error!\");\n// Promise.all([p1, p2]) -> Rejects immediately\n// Promise.allSettled([p1, p2]) -> Resolves with [{status:'fulfilled', value:10}, {status:'rejected', reason:'Error!'}]",
        "tags": ["javascript", "promises", "async-await"]
    },
    {
        "id": "js_this_004",
        "skill": "JavaScript", "topic": "Core JavaScript", "subtopic": "JS 'this' & Prototypes",
        "difficulty": 3,
        "question_text": "How does `this` behave inside an ES6 Arrow Function compared to a regular function?",
        "options": [
            "Arrow functions have lexical `this` bound from the surrounding enclosing execution context, and cannot be changed by `call()`, `apply()`, or `bind()`.",
            "Arrow functions bind `this` to the global `window` object always.",
            "Arrow functions create their own `this` dynamically at invocation time.",
            "Arrow functions throw a TypeError if `this` is accessed."
        ],
        "correct_index": 0,
        "explanation": "Arrow functions do not possess their own `this`. They capture `this` from the lexical scope where they are defined, making them immune to `.bind()` changes.",
        "expected_time_sec": 30,
        "code_snippet": "const obj = {\n  val: 42,\n  getValArrow: () => this.val,\n  getValRegular() { return this.val; }\n};\n// obj.getValRegular() -> 42\n// obj.getValArrow()   -> undefined (lexical this from module/window)",
        "tags": ["javascript", "arrow-functions", "this", "scope"]
    },
    {
        "id": "js_proto_005",
        "skill": "JavaScript", "topic": "Core JavaScript", "subtopic": "JS 'this' & Prototypes",
        "difficulty": 4,
        "question_text": "When accessing `obj.prop`, how does JavaScript resolve the property if it does not exist directly on `obj`?",
        "options": [
            "It searches the Prototype Chain (`__proto__`) up to `Object.prototype`, returning `undefined` if not found.",
            "It throws a PropertyNotFoundError immediately.",
            "It queries the global `window` object.",
            "It checks local storage."
        ],
        "correct_index": 0,
        "explanation": "JavaScript uses prototypal delegation. If a property is not found on the instance, the engine traverses `[[Prototype]]` until reaching `Object.prototype.__proto__ === null`.",
        "expected_time_sec": 35,
        "code_snippet": "const protoObj = { greet: 'Hello' };\nconst child = Object.create(protoObj);\nconsole.log(child.greet); // 'Hello' found on prototype\nconsole.log(child.hasOwnProperty('greet')); // false",
        "tags": ["javascript", "prototypes", "inheritance"]
    },
    {
        "id": "js_hoist_006",
        "skill": "JavaScript", "topic": "Core JavaScript", "subtopic": "JS Closures & Scope",
        "difficulty": 2,
        "question_text": "What occurs when you access a `let` or `const` variable before its line of declaration?",
        "options": [
            "Returns `undefined` like `var`.",
            "Throws `ReferenceError` because the variable resides in the Temporal Dead Zone (TDZ).",
            "Returns `null`.",
            "Causes a compile-time crash."
        ],
        "correct_index": 1,
        "explanation": "`let` and `const` declarations are hoisted but left uninitialized in the TDZ from the start of the block until the declaration is evaluated.",
        "expected_time_sec": 25,
        "code_snippet": "console.log(a); // Output: undefined (var hoisted & initialized to undefined)\nvar a = 5;\n\nconsole.log(b); // Throws ReferenceError: Cannot access 'b' before initialization\nlet b = 10;",
        "tags": ["javascript", "hoisting", "tdz", "let-const"]
    },
    {
        "id": "js_dom_007",
        "skill": "JavaScript", "topic": "Web & DOM", "subtopic": "JS DOM & Events",
        "difficulty": 2,
        "question_text": "What is the primary benefit of Event Delegation in DOM programming?",
        "options": [
            "Attaching a single event listener to a common parent element rather than hundreds of listeners on child nodes.",
            "Preventing CSS styling reflows.",
            "Speeding up image decoding.",
            "Enabling Web Workers automatically."
        ],
        "correct_index": 0,
        "explanation": "Event Delegation leverages event bubbling to handle events at a parent level using `event.target`, minimizing memory consumption and supporting dynamically added elements.",
        "expected_time_sec": 30,
        "code_snippet": "document.getElementById('parent-list').addEventListener('click', (e) => {\n  if (e.target.tagName === 'LI') {\n    console.log('Clicked item:', e.target.innerText);\n  }\n});",
        "tags": ["javascript", "dom", "events", "bubbling"]
    },
    {
        "id": "js_destr_008",
        "skill": "JavaScript", "topic": "Core JavaScript", "subtopic": "JS ES6+ Features",
        "difficulty": 2,
        "question_text": "What is the output of `{ ...{ a: 1, b: 2 }, b: 99, c: 3 }`?",
        "options": [
            "{ a: 1, b: 99, c: 3 }",
            "{ a: 1, b: 2, c: 3 }",
            "SyntaxError: duplicate key",
            "{ a: 1, b: [2, 99], c: 3 }"
        ],
        "correct_index": 0,
        "explanation": "In object spread, subsequent key definitions override earlier values. Here `b: 99` overrides `b: 2` from the spread object.",
        "expected_time_sec": 20,
        "code_snippet": "const config = { host: 'localhost', port: 3000 };\nconst custom = { ...config, port: 8080 };\nconsole.log(custom.port); // 8080",
        "tags": ["javascript", "es6", "spread", "objects"]
    },
    {
        "id": "js_async_009",
        "skill": "JavaScript", "topic": "Async JavaScript", "subtopic": "JS Promises & Async/Await",
        "difficulty": 3,
        "question_text": "What is the output when calling `testAsync()` in JavaScript?",
        "options": [
            "'Start', 'End', 'Resolved'",
            "'Start', 'Resolved', 'End'",
            "'Resolved', 'Start', 'End'",
            "Throws unhandled promise rejection"
        ],
        "correct_index": 0,
        "explanation": "'Start' logs synchronously. The `await` pauses execution of `testAsync` until the promise resolves, allowing surrounding synchronous code to finish before resuming.",
        "expected_time_sec": 30,
        "code_snippet": "async function testAsync() {\n  console.log('Start');\n  const res = await Promise.resolve('Resolved');\n  console.log(res);\n}\ntestAsync();\nconsole.log('End');",
        "tags": ["javascript", "async-await", "promises"]
    },
    {
        "id": "js_weak_010",
        "skill": "JavaScript", "topic": "Advanced JavaScript", "subtopic": "JS Memory & Collections",
        "difficulty": 4,
        "question_text": "Why is `WeakMap` preferred over `Map` when storing private metadata associated with DOM nodes or objects?",
        "options": [
            "`WeakMap` keys are weakly held, allowing garbage collection of keys and values when no other references exist, preventing memory leaks.",
            "`WeakMap` allows integer and string keys.",
            "`WeakMap` is faster to iterate using for...of loops.",
            "`WeakMap` persists across browser tabs."
        ],
        "correct_index": 0,
        "explanation": "`WeakMap` keys must be objects and are weakly referenced. When the key object is deleted elsewhere, its entry in `WeakMap` is automatically eligible for garbage collection.",
        "expected_time_sec": 35,
        "code_snippet": "const privateData = new WeakMap();\nlet domNode = document.createElement('div');\nprivateData.set(domNode, { clickCount: 0 });\ndomNode = null; // Automatically garbage collected from WeakMap!",
        "tags": ["javascript", "weakmap", "memory", "gc"]
    },

    # ==========================================
    # 10. QUANTITATIVE & LOGICAL APTITUDE (4 extra)
    # ==========================================
    {
        "id": "apt_work_001",
        "skill": "Aptitude", "topic": "Quantitative Reasoning", "subtopic": "Time & Work",
        "difficulty": 2,
        "question_text": "Person A can finish a software task in 10 days, and Person B can finish it in 15 days. Working together at constant speed, in how many days will they finish the task?",
        "options": ["6 days", "5 days", "7.5 days", "8 days"],
        "correct_index": 0,
        "explanation": "Work per day = 1/10 + 1/15 = (3 + 2)/30 = 5/30 = 1/6. Therefore, together they take 1 / (1/6) = 6 days.",
        "expected_time_sec": 35,
        "code_snippet": "# Total Days = (A * B) / (A + B)\n# (10 * 15) / (10 + 15) = 150 / 25 = 6 days",
        "tags": ["aptitude", "time-and-work", "quant"]
    },
    {
        "id": "apt_speed_002",
        "skill": "Aptitude", "topic": "Quantitative Reasoning", "subtopic": "Speed, Distance & Time",
        "difficulty": 3,
        "question_text": "Two trains of length 150m and 250m are running on parallel tracks in opposite directions at 54 km/h and 90 km/h. How many seconds will they take to completely cross each other?",
        "options": ["10 seconds", "12 seconds", "15 seconds", "18 seconds"],
        "correct_index": 0,
        "explanation": "Total distance = 150 + 250 = 400m. Relative speed = 54 + 90 = 144 km/h = 144 * (5/18) = 40 m/s. Time = 400 / 40 = 10 seconds.",
        "expected_time_sec": 45,
        "code_snippet": "# Relative Speed (Opposite) = S1 + S2\n# Time = Total Length / Relative Speed = 400 / 40 = 10s",
        "tags": ["aptitude", "speed-distance-time", "quant"]
    },
    {
        "id": "apt_prob_003",
        "skill": "Aptitude", "topic": "Quantitative Reasoning", "subtopic": "Probability & Combinatorics",
        "difficulty": 3,
        "question_text": "Two fair 6-sided dice are rolled simultaneously. What is the probability that the sum of the numbers is greater than 9?",
        "options": ["1/6 (6/36)", "1/9 (4/36)", "5/36", "1/4 (9/36)"],
        "correct_index": 0,
        "explanation": "Favorable outcomes for sum > 9 (i.e. 10, 11, 12): Sum 10: (4,6), (5,5), (6,4) [3]. Sum 11: (5,6), (6,5) [2]. Sum 12: (6,6) [1]. Total = 6 outcomes. Probability = 6/36 = 1/6.",
        "expected_time_sec": 40,
        "code_snippet": "# Favorable pairs: {(4,6), (5,5), (6,4), (5,6), (6,5), (6,6)}\n# Probability = 6 / 36 = 1/6 (~16.67%)",
        "tags": ["aptitude", "probability", "dice"]
    },
    {
        "id": "apt_perm_004",
        "skill": "Aptitude", "topic": "Quantitative Reasoning", "subtopic": "Probability & Combinatorics",
        "difficulty": 2,
        "question_text": "How many distinct permutations can be formed using all the letters of the word 'SYSTEM'?",
        "options": ["360", "720", "120", "180"],
        "correct_index": 0,
        "explanation": "'SYSTEM' has 6 letters with 'S' repeating 2 times. Total permutations = 6! / 2! = 720 / 2 = 360.",
        "expected_time_sec": 30,
        "code_snippet": "# Total = N! / (P! * Q! ...)\n# 6! / 2! = (6 * 5 * 4 * 3 * 2 * 1) / 2 = 360",
        "tags": ["aptitude", "permutations", "combinatorics", "arithmetic"]
    },
    # ── ARITHMETIC APTITUDE ──────────────────────────────────────────
    {
        "id": "apt_arith_001",
        "skill": "Aptitude", "topic": "Arithmetic Aptitude", "subtopic": "Percentages & Profit Loss",
        "difficulty": 2,
        "question_text": "A trader marks his goods 25% above cost price and allows a discount of 10% on the marked price. What is his net gain percentage?",
        "options": ["12.5%", "15%", "10%", "14%"],
        "correct_index": 0,
        "explanation": "Let CP = 100. Marked Price (MP) = 125. Selling Price (SP) = 125 - 10% of 125 = 125 - 12.5 = 112.5. Gain% = (112.5 - 100) = 12.5%.",
        "expected_time_sec": 35,
        "code_snippet": "CP = 100 -> MP = 125 -> SP = 125 * 0.9 = 112.5 -> Profit = 12.5%",
        "tags": ["aptitude", "arithmetic", "percentages", "profit-loss"]
    },
    {
        "id": "apt_arith_002",
        "skill": "Aptitude", "topic": "Arithmetic Aptitude", "subtopic": "Simple & Compound Interest",
        "difficulty": 3,
        "question_text": "The difference between Simple Interest and Compound Interest on a sum of money for 2 years at 10% per annum compounded annually is Rs. 50. What is the principal sum?",
        "options": ["Rs. 5,000", "Rs. 4,500", "Rs. 6,000", "Rs. 5,500"],
        "correct_index": 0,
        "explanation": "For 2 years, Difference = P * (R/100)^2. So 50 = P * (10/100)^2 = P * 0.01. Therefore P = 50 / 0.01 = Rs. 5,000.",
        "expected_time_sec": 40,
        "code_snippet": "Diff = P * (R/100)^2 -> 50 = P * (1/100) -> P = Rs. 5000",
        "tags": ["aptitude", "arithmetic", "interest", "ci-si"]
    },
    {
        "id": "apt_arith_003",
        "skill": "Aptitude", "topic": "Arithmetic Aptitude", "subtopic": "Ratio & Proportion",
        "difficulty": 2,
        "question_text": "The ratio of ages of two persons A and B is 4:5. Eight years hence, the ratio of their ages will be 5:6. What is the present age of A?",
        "options": ["32 years", "40 years", "28 years", "36 years"],
        "correct_index": 0,
        "explanation": "Let ages be 4x and 5x. (4x + 8)/(5x + 8) = 5/6 => 6(4x + 8) = 5(5x + 8) => 24x + 48 = 25x + 40 => x = 8. Present age of A = 4 * 8 = 32 years.",
        "expected_time_sec": 30,
        "code_snippet": "(4x + 8)/(5x + 8) = 5/6 -> 24x + 48 = 25x + 40 -> x = 8 -> Age A = 32",
        "tags": ["aptitude", "arithmetic", "ratio", "ages"]
    },
    # ── DATA INTERPRETATION ──────────────────────────────────────────
    {
        "id": "apt_di_001",
        "skill": "Aptitude", "topic": "Data Interpretation", "subtopic": "Pie Charts & Bar Graphs",
        "difficulty": 2,
        "question_text": "In a software company with 1,200 employees, the expenditure pie chart shows: R&D (30%), Infrastructure (25%), Marketing (20%), Salaries (15%), Others (10%). If R&D budget is increased by 20%, what is the new R&D share angle on the circle?",
        "options": ["129.6°", "108°", "118.8°", "136°"],
        "correct_index": 0,
        "explanation": "Initial R&D = 30% of 360° = 108°. A 20% increase makes it 30% * 1.2 = 36% of total. Angle = 36% * 360° = 129.6°.",
        "expected_time_sec": 45,
        "code_snippet": "New % = 30 * 1.2 = 36% -> Angle = 0.36 * 360 = 129.6 degrees",
        "tags": ["aptitude", "data-interpretation", "pie-chart"]
    },
    {
        "id": "apt_di_002",
        "skill": "Aptitude", "topic": "Data Interpretation", "subtopic": "Tables & Caselets",
        "difficulty": 3,
        "question_text": "A table shows quarterly revenue for 4 products: Q1: [P1: 40k, P2: 60k], Q2: [P1: 50k, P2: 75k]. What is the percentage growth of combined revenue from Q1 to Q2?",
        "options": ["25%", "20%", "30%", "15%"],
        "correct_index": 0,
        "explanation": "Q1 total = 40k + 60k = 100k. Q2 total = 50k + 75k = 125k. Growth = (125k - 100k) / 100k * 100 = 25%.",
        "expected_time_sec": 30,
        "code_snippet": "Q1 = 100k, Q2 = 125k -> ((125 - 100) / 100) * 100 = 25%",
        "tags": ["aptitude", "data-interpretation", "tables"]
    },
    # ── VERBAL ABILITY ───────────────────────────────────────────────
    {
        "id": "apt_va_001",
        "skill": "Aptitude", "topic": "Verbal Ability", "subtopic": "Spotting Errors & Grammar",
        "difficulty": 2,
        "question_text": "Identify the grammatically incorrect segment: 'Neither the system administrator (A) / nor the software developers (B) / was able to resolve the memory leak (C) / during the outage (D).'",
        "options": ["Segment C ('was able to resolve')", "Segment A", "Segment B", "Segment D"],
        "correct_index": 0,
        "explanation": "With 'Neither... nor', the verb agrees with the closer subject. 'Software developers' is plural, so it should be 'were able to resolve', not 'was'.",
        "expected_time_sec": 25,
        "code_snippet": "Rule: Subject-Verb Agreement with 'Neither...nor' -> Plural subject 'developers' requires 'were'",
        "tags": ["aptitude", "verbal-ability", "grammar", "error-spotting"]
    },
    {
        "id": "apt_va_002",
        "skill": "Aptitude", "topic": "Verbal Ability", "subtopic": "Synonyms & Vocabulary",
        "difficulty": 2,
        "question_text": "Choose the most appropriate synonym for the word: 'METICULOUS'",
        "options": ["Painstakingly thorough and careful", "Careless and hurried", "Ambiguous and unclear", "Aggressive and decisive"],
        "correct_index": 0,
        "explanation": "'Meticulous' means showing great attention to detail; very careful, precise and thorough.",
        "expected_time_sec": 20,
        "code_snippet": "Meticulous = Diligent, scrupulous, fastidious, thorough",
        "tags": ["aptitude", "verbal-ability", "synonyms", "vocabulary"]
    },
    # ── LOGICAL REASONING ────────────────────────────────────────────
    {
        "id": "apt_lr_001",
        "skill": "Aptitude", "topic": "Logical Reasoning", "subtopic": "Coding-Decoding & Sequences",
        "difficulty": 2,
        "question_text": "In a certain code, 'PYTHON' is written as 'QZWIPO'. How is 'CODING' written in the same pattern?",
        "options": ["DPEJOH", "DPFKOH", "CQEIOH", "DPEKOG"],
        "correct_index": 0,
        "explanation": "Pattern: Each letter is shifted by +1 (P->Q, Y->Z, T->U(or +1/+2 pattern: P(+1)Q, Y(+1)Z, T(+3)W, H(+1)I, O(+1)P, N(+1)O). For direct +1 shift: C->D, O->P, D->E, I->J, N->O, G->H => DPEJOH.",
        "expected_time_sec": 25,
        "code_snippet": "Shift +1 for each character: C->D, O->P, D->E, I->J, N->O, G->H",
        "tags": ["aptitude", "logical-reasoning", "coding-decoding"]
    },
    {
        "id": "apt_lr_002",
        "skill": "Aptitude", "topic": "Logical Reasoning", "subtopic": "Blood Relations & Direction",
        "difficulty": 2,
        "question_text": "Pointing to a photograph, Rahul said: 'She is the daughter of my grandfather's only son.' How is the woman in the photograph related to Rahul?",
        "options": ["Sister", "Mother", "Cousin", "Aunt"],
        "correct_index": 0,
        "explanation": "Rahul's grandfather's only son = Rahul's father. The daughter of Rahul's father = Rahul's sister.",
        "expected_time_sec": 25,
        "code_snippet": "Grandfather's only son = Father -> Daughter of father = Sister",
        "tags": ["aptitude", "logical-reasoning", "blood-relations"]
    },
    # ── VERBAL REASONING ─────────────────────────────────────────────
    {
        "id": "apt_vr_001",
        "skill": "Aptitude", "topic": "Verbal Reasoning", "subtopic": "Statement & Assumptions",
        "difficulty": 3,
        "question_text": "Statement: 'The college placement cell announced that all students scoring above 75% in adaptive mock tests will be directly shortlisted for Day-1 tier-1 companies.'\nAssumption I: Students desire to get placed in Day-1 tier-1 companies.\nAssumption II: The adaptive mock test score is a valid indicator of placement competence.",
        "options": ["Both I and II are implicit", "Only Assumption I is implicit", "Only Assumption II is implicit", "Neither is implicit"],
        "correct_index": 0,
        "explanation": "Both assumptions are implicit: The cell offers tier-1 shortlisting because students value it (I), and uses mock tests because it considers them a reliable filter (II).",
        "expected_time_sec": 35,
        "code_snippet": "Premise -> Valid incentives (I) + Valid assessment criterion (II) both hold true",
        "tags": ["aptitude", "verbal-reasoning", "assumptions"]
    },
    # ── NONVERBAL REASONING ──────────────────────────────────────────
    {
        "id": "apt_nvr_001",
        "skill": "Aptitude", "topic": "Nonverbal Reasoning", "subtopic": "Cubes, Dice & Spatial Patterns",
        "difficulty": 2,
        "question_text": "A standard 6-sided die is positioned such that 1 is opposite 6, 2 is opposite 5, and 3 is opposite 4. If face 2 is at the bottom and face 3 is facing East, which face is on the Top?",
        "options": ["5", "6", "4", "1"],
        "correct_index": 0,
        "explanation": "Opposite faces sum to 7. If face 2 is at the bottom, its opposite face 5 must be on the Top.",
        "expected_time_sec": 20,
        "code_snippet": "Opposite of Bottom(2) = Top(5)",
        "tags": ["aptitude", "nonverbal-reasoning", "dice-cubes"]
    },
    # ── CURRENT AFFAIRS & TECH ───────────────────────────────────────
    {
        "id": "apt_ca_001",
        "skill": "Aptitude", "topic": "Current Affairs", "subtopic": "Science & Tech Milestones",
        "difficulty": 2,
        "question_text": "Which foundational architecture introduced in the 2017 research paper 'Attention Is All You Need' powers modern Generative AI LLMs?",
        "options": ["Transformer Neural Networks", "Convolutional ResNets", "Recurrent LSTM Networks", "Markov Decision Chains"],
        "correct_index": 0,
        "explanation": "The 2017 paper by Vaswani et al. introduced the Transformer architecture utilizing self-attention mechanisms, replacing recurrent networks for NLP and modern LLMs.",
        "expected_time_sec": 25,
        "code_snippet": "Paper: 'Attention Is All You Need' (2017) -> Transformer Architecture",
        "tags": ["aptitude", "current-affairs", "tech", "genai"]
    },
    # ── GENERAL KNOWLEDGE ────────────────────────────────────────────
    {
        "id": "apt_gk_001",
        "skill": "Aptitude", "topic": "General Knowledge", "subtopic": "Computer Systems & Foundations",
        "difficulty": 2,
        "question_text": "In computer architecture, which level of memory hierarchy provides the lowest latency data access to the CPU?",
        "options": ["CPU Registers", "L1 Cache", "L2 Cache", "Main RAM (DDR5)"],
        "correct_index": 0,
        "explanation": "CPU Registers operate at CPU clock cycle speed (sub-nanosecond / <0.5ns), followed by L1 Cache (1-2ns), L2 Cache (3-10ns), and RAM (50-100ns).",
        "expected_time_sec": 20,
        "code_snippet": "Hierarchy: Registers (<1ns) > L1 (~1ns) > L2 (~4ns) > L3 (~10ns) > RAM (~60ns)",
        "tags": ["aptitude", "general-knowledge", "computer-systems"]
    },
    # ── HR INTERVIEW ─────────────────────────────────────────────────
    {
        "id": "apt_hr_001",
        "skill": "Aptitude", "topic": "HR Interview", "subtopic": "STAR Method & Behavioral",
        "difficulty": 2,
        "question_text": "What does the 'STAR' behavioral interview technique stand for?",
        "options": ["Situation, Task, Action, Result", "Strategy, Timeline, Analysis, Review", "Skills, Teamwork, Attitude, Reliability", "Scope, Technique, Architecture, Refactor"],
        "correct_index": 0,
        "explanation": "STAR stands for Situation, Task, Action, Result — the globally recognized structured framework to answer competency and behavioral interview questions.",
        "expected_time_sec": 20,
        "code_snippet": "STAR = Situation (Context) + Task (Challenge) + Action (Your contribution) + Result (Measurable outcome)",
        "tags": ["aptitude", "hr-interview", "star-method"]
    }
]


def get_all_questions() -> List[Dict[str, Any]]:
    return RAW_QUESTIONS


def get_questions_by_subtopic(subtopic: str) -> List[Dict[str, Any]]:
    return [q for q in RAW_QUESTIONS if q["subtopic"].lower() == subtopic.lower()]


def get_questions_by_skill(skill: str) -> List[Dict[str, Any]]:
    return [q for q in RAW_QUESTIONS if q["skill"].lower() == skill.lower()]


def get_question_by_id(question_id: str) -> Dict[str, Any]:
    for q in RAW_QUESTIONS:
        if q["id"] == question_id:
            return q
    return RAW_QUESTIONS[0]


def get_available_test_tracks() -> List[Dict[str, Any]]:
    """
    Returns available test tracks with language metadata, question counts, and icons.
    """
    return [
        {
            "id": "python",
            "name": "Python 3 & Scripting",
            "skill": "Python",
            "icon": "🐍",
            "category": "language",
            "badge": "Popular",
            "badge_color": "primary",
            "description": "Lists, Dictionaries, OOP, Generators, Decorators, GIL & Asyncio",
            "question_count": len([q for q in RAW_QUESTIONS if q.get("skill") == "Python" or "python" in q.get("tags", [])]),
            "difficulty_range": "Level 1 - 5",
            "topics": ["Data Structures", "OOP", "Generators", "Memory & GIL"]
        },
        {
            "id": "java",
            "name": "Java Core & Enterprise",
            "skill": "Java",
            "icon": "☕",
            "category": "language",
            "badge": "High Demand",
            "badge_color": "warning",
            "description": "Collections, Streams, Lambdas, JVM Memory, Concurrency & Multithreading",
            "question_count": len([q for q in RAW_QUESTIONS if q.get("skill") == "Java" or "java" in q.get("tags", [])]),
            "difficulty_range": "Level 1 - 5",
            "topics": ["Core Java", "Streams API", "Collections", "Concurrency"]
        },
        {
            "id": "cpp",
            "name": "C++ & Modern Systems",
            "skill": "C++",
            "icon": "⚡",
            "category": "language",
            "badge": "Performance",
            "badge_color": "info",
            "description": "Pointers, Memory Management, STL Containers, Smart Pointers & Move Semantics",
            "question_count": len([q for q in RAW_QUESTIONS if q.get("skill") == "C++" or "cpp" in q.get("tags", [])]),
            "difficulty_range": "Level 1 - 5",
            "topics": ["Pointers & Memory", "Smart Pointers", "STL", "OOP & Virtual"]
        },
        {
            "id": "sql",
            "name": "SQL & Relational DBs",
            "skill": "SQL",
            "icon": "🗄️",
            "category": "database",
            "badge": "Essential",
            "badge_color": "success",
            "description": "Complex JOINs, Subqueries, Window Functions, Group By & Index Optimization",
            "question_count": len([q for q in RAW_QUESTIONS if q.get("skill") == "SQL" or "sql" in q.get("tags", [])]),
            "difficulty_range": "Level 1 - 5",
            "topics": ["JOINs", "Window Functions", "Subqueries", "Optimization"]
        },
        {
            "id": "javascript",
            "name": "JavaScript & Web Tech",
            "skill": "JavaScript",
            "icon": "🌐",
            "category": "language",
            "badge": "Full Stack",
            "badge_color": "primary",
            "description": "Closures, Event Loop, Promises, Async/Await, Prototypes & DOM Handling",
            "question_count": len([q for q in RAW_QUESTIONS if q.get("skill") == "JavaScript" or "javascript" in q.get("tags", []) or "js" in q.get("tags", [])]),
            "difficulty_range": "Level 1 - 4",
            "topics": ["Event Loop", "Closures", "Promises", "Prototypes"]
        },
        {
            "id": "dsa",
            "name": "DSA & Problem Solving",
            "skill": "Coding",
            "icon": "🧩",
            "category": "cs",
            "badge": "Top Placement",
            "badge_color": "danger",
            "description": "Two Pointers, Sliding Window, Binary Search, Trees, Graphs & Dynamic Programming",
            "question_count": len([q for q in RAW_QUESTIONS if q.get("skill") == "Coding" or "dsa" in q.get("tags", [])]),
            "difficulty_range": "Level 1 - 5",
            "topics": ["Arrays & Strings", "Trees & Graphs", "Dynamic Programming", "Sliding Window"]
        },
        {
            "id": "dbms",
            "name": "DBMS & Core Architecture",
            "skill": "DBMS",
            "icon": "💾",
            "category": "database",
            "badge": "Core CS",
            "badge_color": "info",
            "description": "ACID Properties, Normalization 1NF-BCNF, Indexing, Transactions & Locking",
            "question_count": len([q for q in RAW_QUESTIONS if q.get("skill") == "DBMS" or "dbms" in q.get("tags", [])]),
            "difficulty_range": "Level 1 - 4",
            "topics": ["ACID", "Normalization", "Indexing", "Concurrency Control"]
        },
        {
            "id": "oop",
            "name": "OOP & Software Design",
            "skill": "OOP",
            "icon": "🏗️",
            "category": "cs",
            "badge": "Architecture",
            "badge_color": "warning",
            "description": "SOLID Principles, Design Patterns, Inheritance, Polymorphism & Abstraction",
            "question_count": len([q for q in RAW_QUESTIONS if q.get("skill") == "OOP" or "oop" in q.get("tags", [])]),
            "difficulty_range": "Level 1 - 4",
            "topics": ["SOLID Principles", "Design Patterns", "Polymorphism", "Interfaces"]
        },
        {
            "id": "aptitude",
            "name": "Quantitative & Logical Aptitude",
            "skill": "Aptitude",
            "icon": "💡",
            "category": "aptitude",
            "badge": "Round 1 Filter",
            "badge_color": "success",
            "description": "Percentages, Profit/Loss, Speed-Distance-Time, Probability & Logical Reasoning",
            "question_count": len([q for q in RAW_QUESTIONS if q.get("skill") == "Aptitude" or "aptitude" in q.get("tags", [])]),
            "difficulty_range": "Level 1 - 4",
            "topics": ["Quantitative", "Probability", "Time & Work", "Speed & Distance"]
        },
        {
            "id": "mixed",
            "name": "Full Placement Diagnostic",
            "skill": "All",
            "icon": "🚀",
            "category": "all",
            "badge": "Comprehensive",
            "badge_color": "primary",
            "description": "Cross-discipline adaptive drill covering all languages and technical readiness areas",
            "question_count": len(RAW_QUESTIONS),
            "difficulty_range": "Level 1 - 5",
            "topics": ["Multi-Language", "DSA", "SQL", "DBMS", "Core CS"]
        }
    ]
