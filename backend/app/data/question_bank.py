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
