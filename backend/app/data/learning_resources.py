from typing import Dict, Any

LEARNING_RESOURCES: Dict[str, Dict[str, Any]] = {
    # ── SQL ─────────────────────────────────────────────────────────────
    "SQL JOINs": {
        "title": "Mastering SQL Relational JOINs",
        "skill": "SQL",
        "topic": "Relational Queries",
        "key_concepts": [
            "INNER JOIN returns only rows with matches in both tables.",
            "LEFT (OUTER) JOIN returns all rows from the left table and NULLs for non-matching right table rows.",
            "FULL OUTER JOIN combines both LEFT and RIGHT outer join behaviors.",
            "CROSS JOIN produces a Cartesian product (M * N rows)."
        ],
        "common_pitfalls": [
            "Using WHERE condition instead of ON clause filters out rows prematurely in LEFT JOINs.",
            "Duplicating rows when joining against non-unique foreign keys without aggregation."
        ],
        "code_example": "SELECT u.name, o.order_date \nFROM users u \nLEFT JOIN orders o ON u.id = o.user_id \nWHERE o.total_amount > 100;",
        "curated_links": [
            {"title": "Visual SQL Joins Guide", "url": "https://mode.com/sql-tutorial/sql-joins/"},
            {"title": "JOIN Performance & Query Optimization", "url": "https://use-the-index-luke.com/sql/joins"}
        ]
    },
    "SQL Subqueries": {
        "title": "Correlated & Nested Subqueries",
        "skill": "SQL",
        "topic": "Advanced Queries",
        "key_concepts": [
            "Scalar subqueries return a single value and can be placed in SELECT or WHERE clauses.",
            "Correlated subqueries reference columns from the outer query and execute once per candidate outer row.",
            "EXISTS is generally faster than IN when the subquery table is large and indexed."
        ],
        "common_pitfalls": [
            "Using IN with NULL values in subqueries causing unexpected empty result sets.",
            "Overusing correlated subqueries when a JOIN with GROUP BY is significantly more performant."
        ],
        "code_example": "SELECT emp_name, salary \nFROM employees e1 \nWHERE salary > (SELECT AVG(salary) FROM employees e2 WHERE e2.department_id = e1.department_id);",
        "curated_links": [
            {"title": "SQL Subqueries Deep Dive", "url": "https://www.w3schools.com/sql/sql_subqueries.asp"}
        ]
    },
    "SQL Window Functions": {
        "title": "SQL Analytical & Window Functions",
        "skill": "SQL",
        "topic": "Advanced Queries",
        "key_concepts": [
            "Window functions perform calculations across a set of table rows related to the current row without collapsing rows.",
            "ROW_NUMBER() assigns consecutive unique integers.",
            "RANK() assigns ranks with gaps on ties; DENSE_RANK() assigns ranks without gaps.",
            "PARTITION BY divides the dataset into independent evaluation windows."
        ],
        "common_pitfalls": [
            "Attempting to use window functions directly inside WHERE or HAVING clauses instead of a CTE/subquery.",
            "Omitting ORDER BY inside OVER() leading to unranked non-deterministic ranges."
        ],
        "code_example": "WITH RankedSalaries AS (\n  SELECT name, department_id, salary,\n         DENSE_RANK() OVER(PARTITION BY department_id ORDER BY salary DESC) as rank_in_dept\n  FROM employees\n)\nSELECT * FROM RankedSalaries WHERE rank_in_dept <= 3;",
        "curated_links": [
            {"title": "PostgreSQL Window Functions Tutorial", "url": "https://www.postgresqltutorial.com/postgresql-window-function/"}
        ]
    },
    "SQL Indexing & Optimization": {
        "title": "Database Query Planning & Indexing Strategies",
        "skill": "SQL",
        "topic": "Performance",
        "key_concepts": [
            "B-Tree indexes provide O(log N) equality and range lookups.",
            "Composite indexes follow the Leftmost Prefix rule.",
            "Covering indexes satisfy queries entirely from the index tree without table heap lookups (Index-Only Scan).",
            "EXPLAIN ANALYZE reveals query cost, actual execution time, and join algorithms (Nested Loop, Hash Join, Merge Join)."
        ],
        "common_pitfalls": [
            "Using functions or operations on indexed columns in WHERE clauses (e.g., WHERE YEAR(date) = 2024), disabling index scans.",
            "Over-indexing tables leading to heavy write amplification on INSERT/UPDATE/DELETE."
        ],
        "code_example": "-- Optimal covering index:\nCREATE INDEX idx_orders_cust_date ON orders(customer_id, order_date) INCLUDE (total_amount);\n\n-- Inspect execution plan:\nEXPLAIN ANALYZE SELECT customer_id, total_amount FROM orders WHERE customer_id = 42;",
        "curated_links": [
            {"title": "Use The Index, Luke! - SQL Indexing Guide", "url": "https://use-the-index-luke.com/"}
        ]
    },

    # ── Coding & DSA ───────────────────────────────────────────────────
    "Recursion": {
        "title": "Recursion Foundations & Call Stack Dynamics",
        "skill": "Coding",
        "topic": "Algorithms",
        "key_concepts": [
            "Every recursive function requires a solid Base Case to prevent StackOverflowError.",
            "Recursive step moves the problem closer to the base case state.",
            "Call stack memory complexity is O(depth of recursion tree)."
        ],
        "common_pitfalls": [
            "Missing base case or incorrect termination condition leading to infinite loops.",
            "Recomputing overlapping subproblems without memoization (exponential O(2^N) explosion)."
        ],
        "code_example": "public int fib(int n, int[] memo) {\n    if (n <= 1) return n;\n    if (memo[n] != 0) return memo[n];\n    return memo[n] = fib(n - 1, memo) + fib(n - 2, memo);\n}",
        "curated_links": [
            {"title": "Recursion to Dynamic Programming", "url": "https://leetcode.com/explore/learn/card/recursion-i/"}
        ]
    },
    "Arrays & Sliding Window": {
        "title": "Array Manipulations & Sliding Window Optimization",
        "skill": "Coding",
        "topic": "Data Structures",
        "key_concepts": [
            "Sliding window converts brute force O(N^2) subarray problems to linear O(N) time.",
            "Prefix sums allow O(1) range sum queries after O(N) preprocessing.",
            "Two pointers technique (opposite ends or fast/slow pointers) optimizes sorted array scans."
        ],
        "common_pitfalls": [
            "Off-by-one errors when adjusting window boundaries (left/right pointers).",
            "Failing to shrink the window when invariant conditions are violated."
        ],
        "code_example": "int left = 0, currentSum = 0, minLen = Integer.MAX_VALUE;\nfor (int right = 0; right < nums.length; right++) {\n    currentSum += nums[right];\n    while (currentSum >= target) {\n        minLen = Math.min(minLen, right - left + 1);\n        currentSum -= nums[left++];\n    }\n}",
        "curated_links": [
            {"title": "Two Pointers & Sliding Window Patterns", "url": "https://github.com/ashishps1/awesome-leetcode-resources"}
        ]
    },
    "Dynamic Programming": {
        "title": "Dynamic Programming & State Transitions",
        "skill": "Coding",
        "topic": "Algorithms",
        "key_concepts": [
            "DP applies to problems with Optimal Substructure and Overlapping Subproblems.",
            "Top-Down approach uses Recursion + Memoization (caching).",
            "Bottom-Up approach uses Iterative Tabulation.",
            "State compression reduces space complexity (e.g., from 2D matrix to 1D array)."
        ],
        "common_pitfalls": [
            "Incorrect base cases in the DP array leading to cascade calculation errors.",
            "Mixing up 0/1 Knapsack (iterate backwards in 1D array) with Unbounded Knapsack (iterate forwards)."
        ],
        "code_example": "// 0/1 Knapsack Bottom-Up Tabulation (Space-Optimized)\nint[] dp = new int[capacity + 1];\nfor (int i = 0; i < n; i++) {\n    for (int w = capacity; w >= weights[i]; w--) {\n        dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);\n    }\n}",
        "curated_links": [
            {"title": "Dynamic Programming Patterns", "url": "https://leetcode.com/discuss/general-discussion/458695/Dynamic-Programming-Patterns"}
        ]
    },

    # ── Java ────────────────────────────────────────────────────────────
    "Collections Framework": {
        "title": "Java Collections Architecture & Internals",
        "skill": "Java",
        "topic": "Collections & Core",
        "key_concepts": [
            "HashMap uses an array of buckets (Node<K,V>) with hash code and equals contract.",
            "Java 8+ converts buckets with >8 elements to Red-Black Trees (TreeNode) for O(log N) lookup.",
            "ConcurrentHashMap uses synchronized bucket locks / CAS for high throughput without full table locks.",
            "TreeSet / TreeMap maintain sorted order via Red-Black BST (O(log N) operations)."
        ],
        "common_pitfalls": [
            "Overriding `equals()` without overriding `hashCode()`, causing lost lookups in HashMap/HashSet.",
            "Modifying a collection while iterating over it, throwing `ConcurrentModificationException`."
        ],
        "code_example": "Map<String, Integer> map = new ConcurrentHashMap<>();\nmap.computeIfAbsent(\"Java\", k -> 100);",
        "curated_links": [
            {"title": "Java HashMap Internals Explained", "url": "https://www.geeksforgeeks.org/internal-working-of-hashmap-java/"}
        ]
    },
    "Multithreading & Concurrency": {
        "title": "Java Concurrency & Thread Synchronization",
        "skill": "Java",
        "topic": "Advanced Core Java",
        "key_concepts": [
            "Thread lifecycle: NEW -> RUNNABLE -> BLOCKED/WAITING -> TERMINATED.",
            "`volatile` ensures visibility of changes across threads by reading/writing directly to main memory.",
            "`synchronized` guarantees mutual exclusion and atomicity.",
            "`ReentrantLock` provides flexible locking, fairness policies, and tryLock."
        ],
        "common_pitfalls": [
            "Deadlocks caused by acquiring multiple locks in inconsistent order.",
            "Race conditions due to non-atomic compound operations (like `count++`)."
        ],
        "code_example": "private final AtomicInteger counter = new AtomicInteger(0);\npublic void increment() {\n    counter.incrementAndGet(); // Thread-safe atomic operation\n}",
        "curated_links": [
            {"title": "Java Concurrency in Practice", "url": "https://docs.oracle.com/javase/tutorial/essential/concurrency/"}
        ]
    },
    "Java Streams & Lambdas": {
        "title": "Functional Programming with Java 8 Streams & Lambdas",
        "skill": "Java",
        "topic": "Core Java",
        "key_concepts": [
            "Streams are sequences of elements supporting sequential and parallel aggregate operations.",
            "Intermediate operations (filter, map, sorted, flatMap) are lazy and return a new Stream.",
            "Terminal operations (collect, reduce, forEach, anyMatch) trigger execution and consume the stream.",
            "Method references (Class::method) provide clean shorthand for lambdas."
        ],
        "common_pitfalls": [
            "Reusing a consumed stream, which throws `IllegalStateException`.",
            "Introducing stateful or non-thread-safe lambdas in parallel streams."
        ],
        "code_example": "List<String> topSkills = skills.stream()\n    .filter(s -> s.getMastery() > 80)\n    .sorted(Comparator.comparing(Skill::getMastery).reversed())\n    .map(Skill::getName)\n    .limit(5)\n    .collect(Collectors.toList());",
        "curated_links": [
            {"title": "Oracle Java Streams Tutorial", "url": "https://docs.oracle.com/javase/8/docs/api/java/util/stream/package-summary.html"}
        ]
    },
    "JVM & Memory Management": {
        "title": "JVM Architecture, Memory Model & Garbage Collection",
        "skill": "Java",
        "topic": "Core Java",
        "key_concepts": [
            "JVM Memory: Heap (Young/Old Generations), Stack (local vars/frames), Metaspace (class metadata).",
            "Garbage Collectors: G1 (region-based, predictable pauses), ZGC/Shenandoah (ultra-low pause <1ms).",
            "Strong, Soft, Weak, and Phantom references control GC retention.",
            "Memory leaks in Java occur when unneeded objects remain strongly reachable from GC roots."
        ],
        "common_pitfalls": [
            "Static collections holding onto large objects indefinitely, preventing GC.",
            "Unclosed resources (Streams, Database connections) causing native resource leaks."
        ],
        "code_example": "// JVM Tuning parameters:\n// java -Xms2g -Xmx4g -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -jar app.jar",
        "curated_links": [
            {"title": "JVM Garbage Collection Handbook", "url": "https://www.baeldung.com/jvm-garbage-collectors"}
        ]
    },

    # ── OOP ─────────────────────────────────────────────────────────────
    "OOP Polymorphism": {
        "title": "Object-Oriented Polymorphism & Dynamic Dispatch",
        "skill": "OOP",
        "topic": "Object Oriented Principles",
        "key_concepts": [
            "Compile-time (Static) Polymorphism: Method Overloading (same name, different parameter signature).",
            "Runtime (Dynamic) Polymorphism: Method Overriding (subclass overrides superclass method).",
            "Virtual Method Table (vtable) handles dynamic binding at runtime in Java/C++."
        ],
        "common_pitfalls": [
            "Assuming private or static methods can be overridden (they are hidden, not overridden).",
            "Violating Liskov Substitution Principle (LSP) by changing expected behavior in derived class."
        ],
        "code_example": "class Animal { void sound() { System.out.println(\"Animal sound\"); } }\nclass Dog extends Animal { @Override void sound() { System.out.println(\"Bark\"); } }\nAnimal a = new Dog(); // Dynamic Dispatch\na.sound(); // prints 'Bark'",
        "curated_links": [
            {"title": "SOLID Principles & Polymorphism", "url": "https://refactoring.guru/design-patterns"}
        ]
    },
    "SOLID Principles": {
        "title": "SOLID Software Architecture Principles",
        "skill": "OOP",
        "topic": "Object Oriented Principles",
        "key_concepts": [
            "S - Single Responsibility: A class should have one reason to change.",
            "O - Open/Closed: Open for extension, closed for modification.",
            "L - Liskov Substitution: Subtypes must be substitutable for their base types.",
            "I - Interface Segregation: Clients shouldn't depend on interfaces they don't use.",
            "D - Dependency Inversion: Depend on abstractions, not concretions."
        ],
        "common_pitfalls": [
            "Creating monolithic 'God classes' that mix database, business logic, and UI.",
            "Hardcoding `new ConcreteService()` instead of injecting interfaces via constructor."
        ],
        "code_example": "// Dependency Inversion with Dependency Injection:\npublic class OrderProcessor {\n    private final PaymentGateway gateway;\n    public OrderProcessor(PaymentGateway gateway) {\n        this.gateway = gateway; // Injected abstraction\n    }\n}",
        "curated_links": [
            {"title": "SOLID Design Principles Explained", "url": "https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design"}
        ]
    },
    "Abstraction & Interfaces": {
        "title": "Abstraction, Interfaces & Abstract Classes",
        "skill": "OOP",
        "topic": "Object Oriented Principles",
        "key_concepts": [
            "Abstract classes can have state (instance variables) and concrete method implementations.",
            "Interfaces represent pure capability contracts and support multiple inheritance in Java.",
            "Java 8+ allows default and static methods in interfaces.",
            "Java 9+ allows private methods in interfaces for helper logic."
        ],
        "common_pitfalls": [
            "Using inheritance when composition (has-a) is cleaner and more flexible.",
            "Overcomplicating simple classes with unnecessary interface hierarchies prematurely."
        ],
        "code_example": "public interface PaymentProcessor {\n    boolean processPayment(double amount);\n    default void logTransaction(String id) {\n        System.out.println(\"Transaction logged: \" + id);\n    }\n}",
        "curated_links": [
            {"title": "Interface vs Abstract Class in Java", "url": "https://www.geeksforgeeks.org/difference-between-abstract-class-and-interface-in-java/"}
        ]
    },
    "Design Patterns": {
        "title": "Gang of Four (GoF) Design Patterns",
        "skill": "OOP",
        "topic": "Design Patterns",
        "key_concepts": [
            "Creational: Singleton (single instance), Factory (object creation abstraction), Builder (step-by-step assembly).",
            "Structural: Adapter (interface bridging), Decorator (dynamic feature wrapping), Proxy (access control).",
            "Behavioral: Observer (pub/sub events), Strategy (interchangeable algorithms), Command (action encapsulation)."
        ],
        "common_pitfalls": [
            "Non-thread-safe Singleton implementations (missing volatile / synchronization).",
            "Over-engineering simple tasks with complex pattern hierarchies."
        ],
        "code_example": "// Thread-safe Enum Singleton:\npublic enum AppConfig {\n    INSTANCE;\n    private String dbUrl = \"jdbc:postgresql://...\";\n    public String getDbUrl() { return dbUrl; }\n}",
        "curated_links": [
            {"title": "Refactoring Guru - Design Patterns", "url": "https://refactoring.guru/design-patterns"}
        ]
    },

    # ── DBMS ────────────────────────────────────────────────────────────
    "Normalization": {
        "title": "Database Normalization (1NF, 2NF, 3NF, BCNF)",
        "skill": "DBMS",
        "topic": "Schema Design",
        "key_concepts": [
            "1NF: Atomic values only, no repeating groups.",
            "2NF: In 1NF and no partial dependencies (non-key attributes fully dependent on candidate keys).",
            "3NF: In 2NF and no transitive dependencies (non-key determining another non-key).",
            "BCNF: For every functional dependency X -> Y, X must be a super key."
        ],
        "common_pitfalls": [
            "Confusing partial dependency (part of composite key) with transitive dependency (non-key to non-key).",
            "Over-normalizing in OLAP/Reporting systems where denormalization improves read throughput."
        ],
        "code_example": "-- 3NF Decomposition\n-- Decompose (StudentID, CourseID, Professor, ProfOffice)\n-- Into (StudentID, CourseID), (CourseID, Professor), (Professor, ProfOffice)",
        "curated_links": [
            {"title": "DBMS Normalization Guide", "url": "https://www.geeksforgeeks.org/introduction-of-database-normalization/"}
        ]
    },
    "ACID Transactions": {
        "title": "ACID Properties & Concurrency Control",
        "skill": "DBMS",
        "topic": "Transactions",
        "key_concepts": [
            "Atomicity: All operations commit or all rollback.",
            "Consistency: Database transitions between valid states preserving schema constraints.",
            "Isolation: Concurrent transactions execute without cross-interference.",
            "Durability: Committed updates survive system crashes via Write-Ahead Logging (WAL)."
        ],
        "common_pitfalls": [
            "Using default READ COMMITTED when non-repeatable reads lead to financial calculation errors.",
            "Long-running transactions holding row/table locks, causing lock contention and timeouts."
        ],
        "code_example": "BEGIN TRANSACTION;\nUPDATE accounts SET balance = balance - 100 WHERE id = 1;\nUPDATE accounts SET balance = balance + 100 WHERE id = 2;\nCOMMIT;",
        "curated_links": [
            {"title": "Transaction Isolation Levels in PostgreSQL", "url": "https://www.postgresql.org/docs/current/transaction-iso.html"}
        ]
    },
    "Database Indexing": {
        "title": "Database Index Architectures & Optimization",
        "skill": "DBMS",
        "topic": "Performance",
        "key_concepts": [
            "Clustered Index: Physically sorts the actual table rows (1 per table, typically Primary Key).",
            "Non-Clustered Index: Independent B-Tree holding pointers (row locators) to data rows.",
            "B+ Trees store records only at leaf nodes, linked sequentially for high-performance range scans."
        ],
        "common_pitfalls": [
            "Creating redundant indexes that mirror leading columns of existing composite indexes.",
            "Ignoring index fragmentation over millions of update operations."
        ],
        "code_example": "CREATE UNIQUE INDEX idx_users_email ON users(email);\nCREATE INDEX idx_orders_status_date ON orders(status, created_at DESC);",
        "curated_links": [
            {"title": "Clustered vs Non-Clustered Indexes", "url": "https://www.geeksforgeeks.org/difference-between-clustered-and-non-clustered-index/"}
        ]
    },

    # ── Aptitude ────────────────────────────────────────────────────────
    "Aptitude & Probability": {
        "title": "Quantitative Aptitude: Combinatorics & Probability",
        "skill": "Aptitude",
        "topic": "Quantitative Reasoning",
        "key_concepts": [
            "Permutations P(n, r) = n! / (n-r)! (Order matters).",
            "Combinations C(n, r) = n! / [r! * (n-r)!] (Order does not matter).",
            "Independent events: P(A ∩ B) = P(A) * P(B).",
            "Complement Rule: P(At least 1 success) = 1 - P(Zero successes)."
        ],
        "common_pitfalls": [
            "Confusing with-replacement vs without-replacement sampling.",
            "Adding probabilities of non-mutually exclusive events without subtracting intersection."
        ],
        "code_example": "Formula: P(At least 1 success) = 1 - P(Zero successes)",
        "curated_links": [
            {"title": "Placement Aptitude Shortcuts", "url": "https://www.indiabix.com/aptitude/questions-and-answers/"}
        ]
    },
    "Speed, Distance & Time": {
        "title": "Speed, Distance, Trains & Relative Velocity",
        "skill": "Aptitude",
        "topic": "Quantitative Reasoning",
        "key_concepts": [
            "Speed = Distance / Time (Unit conversion: 1 km/h = 5/18 m/s).",
            "Average Speed for equal distances: 2xy / (x + y).",
            "Relative speed in opposite directions = S1 + S2; in same direction = |S1 - S2|.",
            "Train crossing a pole covers its own length; crossing a platform covers (Train Length + Platform Length)."
        ],
        "common_pitfalls": [
            "Forgetting unit conversions (km/h vs m/s).",
            "Averaging speeds directly as (x + y)/2 for equal distance journeys."
        ],
        "code_example": "// Relative speed crossing: Time = (L1 + L2) / (Speed1 + Speed2)",
        "curated_links": [
            {"title": "Time and Distance Aptitude Tricks", "url": "https://www.geeksforgeeks.org/time-speed-and-distance/"}
        ]
    },
    "Percentages & Profit-Loss": {
        "title": "Percentages, Profit, Loss & Discount",
        "skill": "Aptitude",
        "topic": "Quantitative Reasoning",
        "key_concepts": [
            "Profit% = (SP - CP) / CP * 100; Loss% = (CP - SP) / CP * 100.",
            "Successive percentage change: a + b + (ab / 100)%.",
            "Marked Price (MP) and Discount: SP = MP * (1 - Discount%/100)."
        ],
        "common_pitfalls": [
            "Calculating profit percentage over Selling Price instead of Cost Price.",
            "Adding two successive 20% discounts to 40% (correct: 20 + 20 - 4 = 36%)."
        ],
        "code_example": "// Multiplier formula: SP = CP * (1 + Profit/100)",
        "curated_links": [
            {"title": "Profit and Loss Formulas", "url": "https://www.indiabix.com/aptitude/profit-and-loss/"}
        ]
    },
    "Number Series & Patterns": {
        "title": "Number Series, Sequences & Logical Patterns",
        "skill": "Aptitude",
        "topic": "Quantitative Reasoning",
        "key_concepts": [
            "Check differences of terms (Arithmetic progression or secondary differences).",
            "Check ratios of terms (Geometric progression).",
            "Check squares and cubes: n^2 ± k, n^3 ± k, n(n+1).",
            "Check alternating interleaved series."
        ],
        "common_pitfalls": [
            "Looking only for single-step arithmetic differences without checking secondary diffs."
        ],
        "code_example": "// Series: 2, 6, 12, 20, 30, 42 -> n*(n+1)",
        "curated_links": [
            {"title": "Number Series Questions", "url": "https://www.indiabix.com/logical-reasoning/number-series/"}
        ]
    },
    "Ratio & Proportion": {
        "title": "Ratios, Proportions & Mixtures",
        "skill": "Aptitude",
        "topic": "Quantitative Reasoning",
        "key_concepts": [
            "Compound Ratio: If A:B = 2:3 and B:C = 4:5, then A:B:C = (2*4):(3*4):(3*5) = 8:12:15.",
            "Alligation Rule: (Cheaper Qty) / (Dearer Qty) = (Dearer Price - Mean) / (Mean - Cheaper Price)."
        ],
        "common_pitfalls": [
            "Combining ratios without equalizing the common bridging variable."
        ],
        "code_example": "// A:B:C calculation helper",
        "curated_links": [
            {"title": "Ratio and Proportion Practice", "url": "https://www.geeksforgeeks.org/ratios-and-proportions/"}
        ]
    },

    # ── Communication ───────────────────────────────────────────────────
    "Technical Communication": {
        "title": "Technical Communication & Interview Precision",
        "skill": "Communication",
        "topic": "Professional Verbal",
        "key_concepts": [
            "STAR Method: Structure every technical behavioral response (Situation, Task, Action, Result).",
            "Translate technical architecture into business outcome metrics (% latency reduction, error reduction).",
            "Active Listening: Clarify requirements, validate assumptions, and think out loud during coding."
        ],
        "common_pitfalls": [
            "Jumping to code without clarifying constraints or discussing time/space tradeoffs with the interviewer.",
            "Giving vague answers without specific technologies or quantified impact."
        ],
        "code_example": "// Framework: Situation -> Challenge -> My Technical Action -> Quantified Metric Result",
        "curated_links": [
            {"title": "STAR Method Technical Interview Guide", "url": "https://www.themuse.com/advice/star-interview-method"}
        ]
    }
}

def get_resource_for_subtopic(subtopic: str) -> Dict[str, Any]:
    for key, val in LEARNING_RESOURCES.items():
        if key.lower() in subtopic.lower() or subtopic.lower() in key.lower():
            return val
    return {
        "title": f"Study Guide for {subtopic}",
        "skill": "Technical",
        "topic": subtopic,
        "key_concepts": [
            f"Understand core principles and theoretical boundaries of {subtopic}.",
            "Review typical interview problem patterns and edge cases.",
            "Practice targeted implementation drills under timed conditions."
        ],
        "common_pitfalls": [
            "Rushing through implementation without validating edge cases and constraints."
        ],
        "code_example": "// Review fundamental implementation patterns\n// and analyze time/space complexity.",
        "curated_links": [
            {"title": "GeeksforGeeks Tutorial", "url": "https://www.geeksforgeeks.org/"},
            {"title": "LeetCode Practice Problems", "url": "https://leetcode.com/problemset/all/"}
        ]
    }
