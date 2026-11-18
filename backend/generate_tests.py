# Python script to generate comprehensive 25 tests (5 per department, 20 MCQs each, 2 coding questions each, and interview topics)
import json

DEPARTMENTS = [
    "Computer Science & Engineering (CSE)",
    "Artificial Intelligence & Data Science (AI-DS)",
    "Electronics & Communication (ECE)",
    "Information Technology (IT)",
    "Electrical & Electronics Engineering (EEE)"
]

# Let's define the 5 test topics for each department
TEST_DEFINITIONS = {
    "Computer Science & Engineering (CSE)": [
        {
            "id": "cse-101",
            "title": "Data Structures & Algorithmic Optimization",
            "description": "Array manipulation, Hash tables, Dynamic Programming, Graphs, and asymptotic complexity.",
            "coding": [
                {
                    "id": "code-cse1-1",
                    "title": "Two Sum with Optimal Index Map",
                    "description": "Given an integer array nums and integer target, return indices of two numbers that add up to target in O(N) time.",
                    "starter_templates": {
                        "python": "def two_sum(nums: list[int], target: int) -> list[int]:\n    seen = {}\n    for i, num in enumerate(nums):\n        comp = target - num\n        if comp in seen:\n            return [seen[comp], i]\n        seen[num] = i\n    return []\n\n# Verification test\nprint(two_sum([2, 7, 11, 15], 9))\n",
                        "javascript": "function twoSum(nums, target) {\n    const map = new Map();\n    for (let i = 0; i < nums.length; i++) {\n        const comp = target - nums[i];\n        if (map.has(comp)) return [map.get(comp), i];\n        map.set(nums[i], i);\n    }\n    return [];\n}\nconsole.log(twoSum([2, 7, 11, 15], 9));\n"
                    },
                    "test_cases": [
                        {"input": "nums = [2, 7, 11, 15], target = 9", "expected": "[0, 1]"},
                        {"input": "nums = [3, 2, 4], target = 6", "expected": "[1, 2]"}
                    ]
                },
                {
                    "id": "code-cse1-2",
                    "title": "LRU Cache Capacity Eviction",
                    "description": "Implement a Least Recently Used (LRU) cache key-value store with fast get and put operations.",
                    "starter_templates": {
                        "python": "class LRUCache:\n    def __init__(self, capacity: int):\n        self.cap = capacity\n        self.cache = {}\n\n    def get(self, key: int) -> int:\n        if key not in self.cache:\n            return -1\n        val = self.cache.pop(key)\n        self.cache[key] = val\n        return val\n\n    def put(self, key: int, value: int) -> None:\n        if key in self.cache:\n            self.cache.pop(key)\n        elif len(self.cache) >= self.cap:\n            oldest = next(iter(self.cache))\n            del self.cache[oldest]\n        self.cache[key] = value\n\nlru = LRUCache(2)\nlru.put(1, 1)\nlru.put(2, 2)\nprint(lru.get(1))\nlru.put(3, 3)\nprint(lru.get(2))\n",
                        "javascript": "class LRUCache {\n    constructor(capacity) {\n        this.capacity = capacity;\n        this.cache = new Map();\n    }\n    get(key) {\n        if (!this.cache.has(key)) return -1;\n        const val = this.cache.get(key);\n        this.cache.delete(key);\n        this.cache.set(key, val);\n        return val;\n    }\n    put(key, value) {\n        if (this.cache.has(key)) this.cache.delete(key);\n        else if (this.cache.size >= this.capacity) {\n            const first = this.cache.keys().next().value;\n            this.cache.delete(first);\n        }\n        this.cache.set(key, value);\n    }\n}\nconst l = new LRUCache(2);\nl.put(1, 1); l.put(2, 2);\nconsole.log(l.get(1));\n"
                    },
                    "test_cases": [
                        {"input": "put(1,1), put(2,2), get(1), put(3,3), get(2)", "expected": "1, -1"}
                    ]
                }
            ],
            "viva_topics": [
                "Explain the amortized time complexity of dynamic array resizing vs linked list insertions.",
                "How does quicksort achieve O(N log N) average time and what pivot strategies avoid worst-case O(N^2)?",
                "When would you choose an Adjacency Matrix over an Adjacency List for sparse vs dense graphs?"
            ]
        },
        {
            "id": "cse-102",
            "title": "Operating Systems & Kernel Architecture",
            "description": "Process scheduling, Virtual Memory, Paging, Deadlocks, Inter-Process Communication, and Mutex Locks.",
            "coding": [
                {
                    "id": "code-cse2-1",
                    "title": "FIFO & LRU Page Fault Simulator",
                    "description": "Calculate total page faults for a reference string given N frame slots under FIFO replacement.",
                    "starter_templates": {
                        "python": "def fifo_page_faults(pages: list[int], frames: int) -> int:\n    memory = set()\n    queue = []\n    faults = 0\n    for p in pages:\n        if p not in memory:\n            if len(memory) == frames:\n                evicted = queue.pop(0)\n                memory.remove(evicted)\n            memory.add(p)\n            queue.append(p)\n            faults += 1\n    return faults\n\nprint('Page Faults:', fifo_page_faults([7, 0, 1, 2, 0, 3, 0, 4, 2, 3], 3))\n",
                        "javascript": "function fifoPageFaults(pages, frames) {\n    const mem = new Set();\n    const q = [];\n    let faults = 0;\n    for (const p of pages) {\n        if (!mem.has(p)) {\n            if (mem.size === frames) {\n                mem.delete(q.shift());\n            }\n            mem.add(p);\n            q.push(p);\n            faults++;\n        }\n    }\n    return faults;\n}\nconsole.log(fifoPageFaults([7, 0, 1, 2, 0, 3, 0, 4, 2, 3], 3));\n"
                    },
                    "test_cases": [
                        {"input": "pages=[7,0,1,2,0,3,0,4,2,3], frames=3", "expected": "7 faults"}
                    ]
                },
                {
                    "id": "code-cse2-2",
                    "title": "Banker's Algorithm Deadlock Safety Check",
                    "description": "Determine whether a system state with allocated and maximum resource matrices is in a safe deadlock-free state.",
                    "starter_templates": {
                        "python": "def is_safe_state(available: list[int], max_need: list[list[int]], alloc: list[list[int]]) -> bool:\n    n = len(alloc)\n    m = len(available)\n    need = [[max_need[i][j] - alloc[i][j] for j in range(m)] for i in range(n)]\n    work = list(available)\n    finish = [False] * n\n    count = 0\n    while count < n:\n        found = False\n        for i in range(n):\n            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):\n                for j in range(m): work[j] += alloc[i][j]\n                finish[i] = True\n                found = True\n                count += 1\n        if not found: break\n    return all(finish)\n\nprint('System Safe:', is_safe_state([3, 3, 2], [[7, 5, 3], [3, 2, 2]], [[0, 1, 0], [2, 0, 0]]))\n",
                        "javascript": "function isSafeState(avail, maxN, alloc) {\n    const n = alloc.length, m = avail.length;\n    const need = alloc.map((r, i) => r.map((c, j) => maxN[i][j] - c));\n    const work = [...avail];\n    const finish = new Array(n).fill(false);\n    let count = 0;\n    while (count < n) {\n        let found = false;\n        for (let i = 0; i < n; i++) {\n            if (!finish[i] && need[i].every((nd, j) => nd <= work[j])) {\n                for (let j = 0; j < m; j++) work[j] += alloc[i][j];\n                finish[i] = true; found = true; count++;\n            }\n        }\n        if (!found) break;\n    }\n    return finish.every(Boolean);\n}\nconsole.log(isSafeState([3, 3, 2], [[7, 5, 3], [3, 2, 2]], [[0, 1, 0], [2, 0, 0]]));\n"
                    },
                    "test_cases": [
                        {"input": "avail=[3,3,2], 2 processes", "expected": "True"}
                    ]
                }
            ],
            "viva_topics": [
                "Explain the 4 necessary conditions for a Deadlock to occur according to Coffman.",
                "How does the Translation Lookaside Buffer (TLB) accelerate virtual-to-physical address translation?",
                "What is the difference between preemptive Priority Scheduling and Round Robin in kernel scheduling?"
            ]
        },
        {
            "id": "cse-103",
            "title": "Computer Networks & Distributed Protocols",
            "description": "TCP/IP, Congestion Control, DNS, HTTP/3, Routing Algorithms, and Distributed Consensus.",
            "coding": [
                {
                    "id": "code-cse3-1",
                    "title": "IPv4 Subnet Address Range Calculator",
                    "description": "Given an IP address in CIDR format (e.g., '192.168.1.55/24'), compute network address, broadcast address, and total usable hosts.",
                    "starter_templates": {
                        "python": "def calc_subnet(cidr: str) -> dict:\n    ip_str, mask_str = cidr.split('/')\n    mask = int(mask_str)\n    octets = [int(x) for x in ip_str.split('.')]\n    ip_int = (octets[0] << 24) + (octets[1] << 16) + (octets[2] << 8) + octets[3]\n    netmask_int = ((1 << 32) - 1) ^ ((1 << (32 - mask)) - 1)\n    net_int = ip_int & netmask_int\n    bcast_int = net_int | (~netmask_int & 0xFFFFFFFF)\n    def to_ip(val): return f\"{(val >> 24) & 255}.{(val >> 16) & 255}.{(val >> 8) & 255}.{val & 255}\"\n    return {\n        'network': to_ip(net_int),\n        'broadcast': to_ip(bcast_int),\n        'usable_hosts': (2 ** (32 - mask)) - 2\n    }\n\nprint(calc_subnet('192.168.1.55/24'))\n",
                        "javascript": "function calcSubnet(cidr) {\n    const [ip, mStr] = cidr.split('/');\n    const mask = parseInt(mStr, 10);\n    const usable = Math.pow(2, 32 - mask) - 2;\n    return { cidr, usable_hosts: usable };\n}\nconsole.log(calcSubnet('192.168.1.55/24'));\n"
                    },
                    "test_cases": [
                        {"input": "'192.168.1.55/24'", "expected": "network: 192.168.1.0, usable: 254"}
                    ]
                },
                {
                    "id": "code-cse3-2",
                    "title": "Token Bucket Rate Limiter",
                    "description": "Implement a token bucket algorithm to rate limit API network requests with burst capacity.",
                    "starter_templates": {
                        "python": "import time\n\nclass TokenBucket:\n    def __init__(self, capacity: int, fill_rate: float):\n        self.capacity = capacity\n        self.fill_rate = fill_rate\n        self.tokens = capacity\n        self.last_update = time.time()\n\n    def allow_request(self, tokens_needed: int = 1) -> bool:\n        now = time.time()\n        elapsed = now - self.last_update\n        self.tokens = min(self.capacity, self.tokens + elapsed * self.fill_rate)\n        self.last_update = now\n        if self.tokens >= tokens_needed:\n            self.tokens -= tokens_needed\n            return True\n        return False\n\nbucket = TokenBucket(capacity=5, fill_rate=2.0)\nprint('Req 1:', bucket.allow_request(1))\nprint('Req 2:', bucket.allow_request(1))\n",
                        "javascript": "class TokenBucket {\n    constructor(capacity, fillRate) {\n        this.capacity = capacity;\n        this.fillRate = fillRate;\n        this.tokens = capacity;\n        this.last = Date.now();\n    }\n    allow() {\n        const now = Date.now();\n        this.tokens = Math.min(this.capacity, this.tokens + ((now - this.last)/1000) * this.fillRate);\n        this.last = now;\n        if (this.tokens >= 1) { this.tokens--; return true; }\n        return false;\n    }\n}\nconst tb = new TokenBucket(5, 2);\nconsole.log(tb.allow());\n"
                    },
                    "test_cases": [
                        {"input": "capacity=5, fill=2", "expected": "Req 1: True, Req 2: True"}
                    ]
                }
            ],
            "viva_topics": [
                "Describe the TCP 3-way handshake and 4-way termination with TIME_WAIT significance.",
                "How does BGP (Border Gateway Protocol) route packets across autonomous systems?",
                "What solves Head-of-Line (HoL) blocking in HTTP/3 with QUIC UDP vs HTTP/2 over TCP?"
            ]
        },
        {
            "id": "cse-104",
            "title": "Database Internals & Index Optimization",
            "description": "B+ Trees, LSM Trees, ACID transactions, Write-Ahead Logging (WAL), isolation levels, and Query Planning.",
            "coding": [
                {
                    "id": "code-cse4-1",
                    "title": "B-Tree Binary Search on Sorted Node Keys",
                    "description": "Find the key index or target child branch in a B-Tree internal node holding M sorted keys.",
                    "starter_templates": {
                        "python": "def find_btree_child(keys: list[int], target: int) -> int:\n    low, high = 0, len(keys) - 1\n    idx = len(keys)\n    while low <= high:\n        mid = (low + high) // 2\n        if keys[mid] > target:\n            idx = mid\n            high = mid - 1\n        else:\n            low = mid + 1\n    return idx\n\nprint('Branch index:', find_btree_child([10, 20, 30, 40, 50], 25))\n",
                        "javascript": "function findBtreeChild(keys, target) {\n    let idx = keys.findIndex(k => k > target);\n    return idx === -1 ? keys.length : idx;\n}\nconsole.log(findBtreeChild([10, 20, 30, 40, 50], 25));\n"
                    },
                    "test_cases": [
                        {"input": "keys=[10,20,30,40,50], target=25", "expected": "2"}
                    ]
                },
                {
                    "id": "code-cse4-2",
                    "title": "Write-Ahead Log (WAL) Redo Recovery",
                    "description": "Simulate WAL commit recovery by replaying committed transactions and ignoring uncommitted ones.",
                    "starter_templates": {
                        "python": "def replay_wal(records: list[dict]) -> dict:\n    state = {}\n    committed_txns = set()\n    for r in records:\n        if r['type'] == 'COMMIT': committed_txns.add(r['txn'])\n    for r in records:\n        if r['type'] == 'SET' and r['txn'] in committed_txns:\n            state[r['key']] = r['val']\n    return state\n\nlog = [\n    {'type': 'SET', 'txn': 1, 'key': 'a', 'val': 100},\n    {'type': 'COMMIT', 'txn': 1},\n    {'type': 'SET', 'txn': 2, 'key': 'b', 'val': 200}\n]\nprint('Recovered State:', replay_wal(log))\n",
                        "javascript": "function replayWal(records) {\n    const state = {};\n    const committed = new Set(records.filter(r => r.type === 'COMMIT').map(r => r.txn));\n    records.forEach(r => {\n        if (r.type === 'SET' && committed.has(r.txn)) state[r.key] = r.val;\n    });\n    return state;\n}\nconsole.log(replayWal([{'type':'SET','txn':1,'key':'a','val':100},{'type':'COMMIT','txn':1}]));\n"
                    },
                    "test_cases": [
                        {"input": "log with Txn 1 committed and Txn 2 uncommitted", "expected": "{'a': 100}"}
                    ]
                }
            ],
            "viva_topics": [
                "Contrast B+ Trees used in relational databases against LSM Trees used in Cassandra/RocksDB.",
                "Explain the differences between Read Committed and Serializable isolation levels and how Phantom Reads occur.",
                "How does Multi-Version Concurrency Control (MVCC) eliminate read-write locking conflicts?"
            ]
        },
        {
            "id": "cse-105",
            "title": "Compiler Design & Automata Theory",
            "description": "Lexical analysis, DFA/NFA, LL(1) / LR(1) parsing, Intermediate Representation (IR), and Code Optimization.",
            "coding": [
                {
                    "id": "code-cse5-1",
                    "title": "Lexical Tokenizer for Math Expressions",
                    "description": "Tokenize an arithmetic string into tokens (NUMBER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN).",
                    "starter_templates": {
                        "python": "import re\n\ndef tokenize(expr: str) -> list[tuple[str, str]]:\n    spec = [\n        ('NUMBER', r'\\d+(\\.\\d+)?'),\n        ('PLUS', r'\\+'),\n        ('MINUS', r'-'),\n        ('MUL', r'\\*'),\n        ('DIV', r'/'),\n        ('LPAREN', r'\\('),\n        ('RPAREN', r'\\)'),\n        ('SKIP', r'\\s+'),\n    ]\n    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in spec)\n    tokens = []\n    for mo in re.finditer(tok_regex, expr):\n        kind = mo.lastgroup\n        val = mo.group()\n        if kind != 'SKIP': tokens.append((kind, val))\n    return tokens\n\nprint(tokenize('3 + 4 * (10 - 2)'))\n",
                        "javascript": "function tokenize(expr) {\n    return expr.match(/\\d+|[+\\-*/()]/g) || [];\n}\nconsole.log(tokenize('3 + 4 * (10 - 2)'));\n"
                    },
                    "test_cases": [
                        {"input": "'3 + 4 * 2'", "expected": "Tokens parsed successfully"}
                    ]
                },
                {
                    "id": "code-cse5-2",
                    "title": "Reverse Polish Notation (RPN) Stack Evaluator",
                    "description": "Evaluate the arithmetic value of an expression in postfix / Reverse Polish Notation.",
                    "starter_templates": {
                        "python": "def eval_rpn(tokens: list[str]) -> int:\n    stack = []\n    for t in tokens:\n        if t in {'+', '-', '*', '/'}:\n            b = stack.pop()\n            a = stack.pop()\n            if t == '+': stack.append(a + b)\n            elif t == '-': stack.append(a - b)\n            elif t == '*': stack.append(a * b)\n            elif t == '/': stack.append(int(a / b))\n        else:\n            stack.append(int(t))\n    return stack[0]\n\nprint('Result:', eval_rpn(['2', '1', '+', '3', '*']))\n",
                        "javascript": "function evalRPN(tokens) {\n    const s = [];\n    for (const t of tokens) {\n        if (['+','-','*','/'].includes(t)) {\n            const b = s.pop(), a = s.pop();\n            if (t === '+') s.push(a + b);\n            if (t === '-') s.push(a - b);\n            if (t === '*') s.push(a * b);\n            if (t === '/') s.push(Math.trunc(a / b));\n        } else s.push(Number(t));\n    }\n    return s[0];\n}\nconsole.log(evalRPN(['2', '1', '+', '3', '*']));\n"
                    },
                    "test_cases": [
                        {"input": "['2', '1', '+', '3', '*']", "expected": "9"}
                    ]
                }
            ],
            "viva_topics": [
                "What is the Chomsky Hierarchy of grammars and which class can standard parser generators handle?",
                "Explain the role of Static Single Assignment (SSA) form in modern optimizing compilers like LLVM.",
                "How does Shift-Reduce conflict resolution work in LR(1) and LALR(1) parsing tables?"
            ]
        }
    ],

    "Artificial Intelligence & Data Science (AI-DS)": [
        {
            "id": "aids-201",
            "title": "Machine Learning Foundations & Supervised Models",
            "description": "Loss functions, Gradient Descent, Decision Trees, Ensembles (XGBoost, Random Forest), Bias-Variance tradeoff.",
            "coding": [
                {
                    "id": "code-aids1-1",
                    "title": "Linear Regression Gradient Descent Optimizer",
                    "description": "Implement univariate gradient descent to find optimal slope m and intercept b for given (X, y) points.",
                    "starter_templates": {
                        "python": "def train_linear_regression(X: list[float], y: list[float], lr=0.01, epochs=100) -> tuple[float, float]:\n    m, b = 0.0, 0.0\n    n = len(X)\n    for _ in range(epochs):\n        dm = sum(-2 * X[i] * (y[i] - (m * X[i] + b)) for i in range(n)) / n\n        db = sum(-2 * (y[i] - (m * X[i] + b)) for i in range(n)) / n\n        m -= lr * dm\n        b -= lr * db\n    return round(m, 2), round(b, 2)\n\nprint('Fitted (m, b):', train_linear_regression([1, 2, 3, 4], [2, 4, 6, 8]))\n",
                        "javascript": "function trainLR(X, y, lr=0.01, epochs=100) {\n    let m = 0, b = 0, n = X.length;\n    for (let e = 0; e < epochs; e++) {\n        let dm = 0, db = 0;\n        for (let i = 0; i < n; i++) {\n            let err = y[i] - (m * X[i] + b);\n            dm += -2 * X[i] * err; db += -2 * err;\n        }\n        m -= lr * (dm / n); b -= lr * (db / n);\n    }\n    return [m.toFixed(2), b.toFixed(2)];\n}\nconsole.log(trainLR([1, 2, 3, 4], [2, 4, 6, 8]));\n"
                    },
                    "test_cases": [
                        {"input": "X=[1,2,3,4], y=[2,4,6,8]", "expected": "m ~ 2.0, b ~ 0.0"}
                    ]
                },
                {
                    "id": "code-aids1-2",
                    "title": "K-Means Centroid Assignment Step",
                    "description": "Assign data points to the closest cluster centroid using Euclidean distance.",
                    "starter_templates": {
                        "python": "def assign_clusters(points: list[list[float]], centroids: list[list[float]]) -> list[int]:\n    assignments = []\n    for p in points:\n        distances = [sum((p[d] - c[d]) ** 2 for d in range(len(p))) for c in centroids]\n        closest = distances.index(min(distances))\n        assignments.append(closest)\n    return assignments\n\npts = [[1.0, 1.0], [5.0, 5.0], [1.5, 2.0]]\ncenters = [[1.0, 1.0], [5.0, 5.0]]\nprint('Cluster IDs:', assign_clusters(pts, centers))\n",
                        "javascript": "function assignClusters(pts, centers) {\n    return pts.map(p => {\n        const dists = centers.map(c => Math.hypot(p[0]-c[0], p[1]-c[1]));\n        return dists.indexOf(Math.min(...dists));\n    });\n}\nconsole.log(assignClusters([[1,1],[5,5],[1.5,2]], [[1,1],[5,5]]));\n"
                    },
                    "test_cases": [
                        {"input": "3 points with 2 centroids", "expected": "[0, 1, 0]"}
                    ]
                }
            ],
            "viva_topics": [
                "Explain the mathematical formulation of L1 Lasso vs L2 Ridge regularization and their effect on sparsity.",
                "How does XGBoost compute split points using the gradient and hessian of the loss function?",
                "What is the ROC-AUC curve and why is it preferred over raw accuracy on imbalanced datasets?"
            ]
        },
        {
            "id": "aids-202",
            "title": "Deep Learning & Neural Architectures",
            "description": "Backpropagation, activation functions (ReLU, GELU), Optimizers (Adam, RMSprop), Batch Normalization, and Dropout.",
            "coding": [
                {
                    "id": "code-aids2-1",
                    "title": "Feedforward Dense Layer with ReLU",
                    "description": "Implement matrix multiplication for a dense neural network layer with ReLU activation.",
                    "starter_templates": {
                        "python": "def dense_relu(inputs: list[float], weights: list[list[float]], biases: list[float]) -> list[float]:\n    outputs = []\n    for col_w, b in zip(weights, biases):\n        val = sum(x * w for x, w in zip(inputs, col_w)) + b\n        outputs.append(max(0.0, val))\n    return outputs\n\nx = [1.0, 2.0]\nw = [[0.5, -0.5], [1.5, 0.5]]\nb = [0.1, -0.2]\nprint('Activations:', dense_relu(x, w, b))\n",
                        "javascript": "function denseRelu(x, w, b) {\n    return w.map((colW, i) => Math.max(0, colW.reduce((sum, wt, j) => sum + x[j]*wt, 0) + b[i]));\n}\nconsole.log(denseRelu([1, 2], [[0.5, -0.5], [1.5, 0.5]], [0.1, -0.2]));\n"
                    },
                    "test_cases": [
                        {"input": "inputs=[1.0, 2.0]", "expected": "Non-negative activations with ReLU applied"}
                    ]
                },
                {
                    "id": "code-aids2-2",
                    "title": "Softmax & Categorical Cross-Entropy Loss",
                    "description": "Compute numerically stable Softmax probabilities and multi-class Cross-Entropy Loss.",
                    "starter_templates": {
                        "python": "import math\n\ndef softmax_cross_entropy(logits: list[float], target_idx: int) -> tuple[list[float], float]:\n    max_logit = max(logits)\n    exp_logits = [math.exp(l - max_logit) for l in logits]\n    sum_exp = sum(exp_logits)\n    probs = [e / sum_exp for e in exp_logits]\n    loss = -math.log(max(probs[target_idx], 1e-12))\n    return [round(p, 4) for p in probs], round(loss, 4)\n\nprobs, loss = softmax_cross_entropy([2.0, 1.0, 0.1], target_idx=0)\nprint('Probs:', probs, 'Loss:', loss)\n",
                        "javascript": "function softmaxLoss(logits, target) {\n    const maxL = Math.max(...logits);\n    const exps = logits.map(l => Math.exp(l - maxL));\n    const sumE = exps.reduce((a, b) => a + b, 0);\n    const probs = exps.map(e => e / sumE);\n    const loss = -Math.log(Math.max(probs[target], 1e-12));\n    return { probs, loss };\n}\nconsole.log(softmaxLoss([2, 1, 0.1], 0));\n"
                    },
                    "test_cases": [
                        {"input": "logits=[2.0, 1.0, 0.1], target=0", "expected": "Highest prob at index 0, low cross-entropy loss"}
                    ]
                }
            ],
            "viva_topics": [
                "Explain the Vanishing Gradient problem and how Residual Connections (ResNets) solve it.",
                "How does the Adam optimizer combine momentum with adaptive learning rates per parameter?",
                "What is Batch Normalization doing during training vs inference (running mean/var)?"
            ]
        },
        {
            "id": "aids-203",
            "title": "Generative AI, LLMs & Transformer Models",
            "description": "Self-Attention, Multi-Head Attention, RoPE embeddings, KV Cache, RAG architectures, and RLHF.",
            "coding": [
                {
                    "id": "code-aids3-1",
                    "title": "Scaled Dot-Product Attention Core",
                    "description": "Calculate scaled dot-product attention scores Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V for single head.",
                    "starter_templates": {
                        "python": "import math\n\ndef scaled_dot_product_attention(q: list[float], k_list: list[list[float]], v_list: list[list[float]]) -> list[float]:\n    d_k = len(q)\n    scores = [sum(qi * ki for qi, ki in zip(q, k)) / math.sqrt(d_k) for k in k_list]\n    exp_s = [math.exp(s - max(scores)) for s in scores]\n    weights = [e / sum(exp_s) for e in exp_s]\n    dim_v = len(v_list[0])\n    output = [sum(weights[i] * v_list[i][d] for i in range(len(v_list))) for d in range(dim_v)]\n    return [round(x, 4) for x in output]\n\nQ = [1.0, 0.0]\nK = [[1.0, 0.0], [0.0, 1.0]]\nV = [[2.0, 4.0], [6.0, 8.0]]\nprint('Context Vector:', scaled_dot_product_attention(Q, K, V))\n",
                        "javascript": "function attention(q, K, V) {\n    const dk = q.length;\n    const scores = K.map(k => q.reduce((acc, qi, i) => acc + qi*k[i], 0) / Math.sqrt(dk));\n    const maxS = Math.max(...scores);\n    const exps = scores.map(s => Math.exp(s - maxS));\n    const sumE = exps.reduce((a, b) => a + b, 0);\n    const w = exps.map(e => e / sumE);\n    return [0, 1].map(d => w.reduce((acc, wt, i) => acc + wt * V[i][d], 0));\n}\nconsole.log(attention([1,0], [[1,0],[0,1]], [[2,4],[6,8]]));\n"
                    },
                    "test_cases": [
                        {"input": "Q=[1,0], attends primarily to K[0]", "expected": "Context vector ~ [2.0, 4.0]"}
                    ]
                },
                {
                    "id": "code-aids3-2",
                    "title": "Cosine Similarity Vector Embedding Ranker",
                    "description": "Rank documents by cosine similarity against a query vector for RAG retrieval.",
                    "starter_templates": {
                        "python": "import math\n\ndef rank_docs_cosine(query: list[float], doc_embeddings: list[list[float]]) -> list[int]:\n    def norm(v): return math.sqrt(sum(x*x for x in v)) or 1e-12\n    q_norm = norm(query)\n    sims = []\n    for idx, doc in enumerate(doc_embeddings):\n        dot = sum(qi * di for qi, di in zip(query, doc))\n        sim = dot / (q_norm * norm(doc))\n        sims.append((sim, idx))\n    sims.sort(key=lambda x: x[0], reverse=True)\n    return [idx for _, idx in sims]\n\nq = [1.0, 1.0, 0.0]\ndocs = [[1.0, 1.0, 0.0], [0.0, 0.0, 1.0], [0.9, 0.8, 0.1]]\nprint('Ranked Doc Indices:', rank_docs_cosine(q, docs))\n",
                        "javascript": "function rankDocs(q, docs) {\n    const norm = v => Math.hypot(...v) || 1e-9;\n    const qN = norm(q);\n    return docs.map((d, idx) => {\n        const dot = q.reduce((s, qi, i) => s + qi * d[i], 0);\n        return { idx, sim: dot / (qN * norm(d)) };\n    }).sort((a, b) => b.sim - a.sim).map(x => x.idx);\n}\nconsole.log(rankDocs([1,1,0], [[1,1,0],[0,0,1],[0.9,0.8,0.1]]));\n"
                    },
                    "test_cases": [
                        {"input": "q=[1,1,0] against 3 docs", "expected": "Index 0 ranked first"}
                    ]
                }
            ],
            "viva_topics": [
                "Explain how FlashAttention avoids high memory bandwidth bottlenecks during attention computation.",
                "What is the difference between dense retrieval with vector embeddings vs BM25 sparse keyword search?",
                "How does speculative decoding accelerate LLM token generation without degrading output accuracy?"
            ]
        },
        {
            "id": "aids-204",
            "title": "Computer Vision & Visual Pattern Recognition",
            "description": "Convolutional Neural Networks (CNNs), Spatial Pooling, Edge Detection, Object Detection (YOLO), and Segmentation.",
            "coding": [
                {
                    "id": "code-aids4-1",
                    "title": "2D Convolution Kernel Filter Operation",
                    "description": "Apply a 3x3 convolution kernel over an image matrix without padding to compute feature map.",
                    "starter_templates": {
                        "python": "def conv2d(img: list[list[float]], kernel: list[list[float]]) -> list[list[float]]:\n    h, w = len(img), len(img[0])\n    kh, kw = len(kernel), len(kernel[0])\n    out_h, out_w = h - kh + 1, w - kw + 1\n    out = []\n    for i in range(out_h):\n        row = []\n        for j in range(out_w):\n            val = sum(img[i + ki][j + kj] * kernel[ki][kj] for ki in range(kh) for kj in range(kw))\n            row.append(round(val, 2))\n        out.append(row)\n    return out\n\npic = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\nedge = [[0, -1], [1, 0]]\nprint('Feature Map:', conv2d(pic, edge))\n",
                        "javascript": "function conv2d(img, k) {\n    const h = img.length, w = img[0].length;\n    const kh = k.length, kw = k[0].length;\n    const out = [];\n    for (let i = 0; i <= h - kh; i++) {\n        const row = [];\n        for (let j = 0; j <= w - kw; j++) {\n            let val = 0;\n            for (let ki = 0; ki < kh; ki++) for (let kj = 0; kj < kw; kj++) val += img[i+ki][j+kj] * k[ki][kj];\n            row.push(val);\n        }\n        out.push(row);\n    }\n    return out;\n}\nconsole.log(conv2d([[1,2,3],[4,5,6],[7,8,9]], [[0,-1],[1,0]]));\n"
                    },
                    "test_cases": [
                        {"input": "3x3 image with 2x2 kernel", "expected": "2x2 output feature matrix"}
                    ]
                },
                {
                    "id": "code-aids4-2",
                    "title": "Intersection over Union (IoU) Bounding Box Calculator",
                    "description": "Compute the IoU score between two bounding boxes [x1, y1, x2, y2] for object detection accuracy.",
                    "starter_templates": {
                        "python": "def calc_iou(boxA: list[float], boxB: list[float]) -> float:\n    xA = max(boxA[0], boxB[0])\n    yA = max(boxA[1], boxB[1])\n    xB = min(boxA[2], boxB[2])\n    yB = min(boxA[3], boxB[3])\n    inter_area = max(0.0, xB - xA) * max(0.0, yB - yA)\n    boxA_area = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])\n    boxB_area = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])\n    union = boxA_area + boxB_area - inter_area\n    return round(inter_area / union if union > 0 else 0.0, 4)\n\nprint('IoU:', calc_iou([0, 0, 10, 10], [5, 5, 15, 15]))\n",
                        "javascript": "function calcIoU(a, b) {\n    const xA = Math.max(a[0], b[0]), yA = Math.max(a[1], b[1]);\n    const xB = Math.min(a[2], b[2]), yB = Math.min(a[3], b[3]);\n    const inter = Math.max(0, xB - xA) * Math.max(0, yB - yA);\n    const union = (a[2]-a[0])*(a[3]-a[1]) + (b[2]-b[0])*(b[3]-b[1]) - inter;\n    return union > 0 ? (inter / union).toFixed(4) : 0;\n}\nconsole.log(calcIoU([0,0,10,10], [5,5,15,15]));\n"
                    },
                    "test_cases": [
                        {"input": "[0,0,10,10] and [5,5,15,15]", "expected": "0.1429"}
                    ]
                }
            ],
            "viva_topics": [
                "How does Non-Maximum Suppression (NMS) clean up overlapping candidate bounding boxes in YOLO?",
                "What is the mathematical principle of Sobel edge detection using spatial gradient convolutions?",
                "Explain the architecture of Vision Transformers (ViT) and how image patches are converted to sequence tokens."
            ]
        },
        {
            "id": "aids-205",
            "title": "Natural Language Processing & Information Retrieval",
            "description": "Tokenization, Word2Vec, TF-IDF, Transformer tokenizers, Named Entity Recognition (NER), and Semantic Search.",
            "coding": [
                {
                    "id": "code-aids5-1",
                    "title": "TF-IDF Term Weighting Calculator",
                    "description": "Compute Term Frequency - Inverse Document Frequency (TF-IDF) for a term across a small corpus of documents.",
                    "starter_templates": {
                        "python": "import math\n\ndef compute_tfidf(term: str, doc: list[str], corpus: list[list[str]]) -> float:\n    tf = doc.count(term) / len(doc) if doc else 0\n    docs_with_term = sum(1 for d in corpus if term in d)\n    idf = math.log((1 + len(corpus)) / (1 + docs_with_term)) + 1\n    return round(tf * idf, 4)\n\ncorp = [['apple', 'banana', 'apple'], ['banana', 'orange'], ['grape']]\nprint('TF-IDF for apple in doc 0:', compute_tfidf('apple', corp[0], corp))\n",
                        "javascript": "function tfidf(term, doc, corpus) {\n    const tf = doc.filter(w => w === term).length / doc.length;\n    const docsWithTerm = corpus.filter(d => d.includes(term)).length;\n    const idf = Math.log((1 + corpus.length) / (1 + docsWithTerm)) + 1;\n    return (tf * idf).toFixed(4);\n}\nconsole.log(tfidf('apple', ['apple','banana','apple'], [['apple','banana','apple'],['banana']]));\n"
                    },
                    "test_cases": [
                        {"input": "term='apple', doc=['apple','banana','apple']", "expected": "High positive TF-IDF weight"}
                    ]
                },
                {
                    "id": "code-aids5-2",
                    "title": "N-gram Language Sequence Extractor",
                    "description": "Extract all consecutive n-grams of size N from a tokenized text sequence.",
                    "starter_templates": {
                        "python": "def extract_ngrams(tokens: list[str], n: int) -> list[list[str]]:\n    if len(tokens) < n: return []\n    return [tokens[i:i + n] for i in range(len(tokens) - n + 1)]\n\nwords = ['natural', 'language', 'processing', 'is', 'fascinating']\nprint('Bigrams:', extract_ngrams(words, 2))\n",
                        "javascript": "function ngrams(tokens, n) {\n    const res = [];\n    for (let i = 0; i <= tokens.length - n; i++) res.push(tokens.slice(i, i + n));\n    return res;\n}\nconsole.log(ngrams(['natural', 'language', 'processing'], 2));\n"
                    },
                    "test_cases": [
                        {"input": "tokens=['natural', 'language', 'processing'], n=2", "expected": "[['natural', 'language'], ['language', 'processing']]"}
                    ]
                }
            ],
            "viva_topics": [
                "Contrast Word2Vec CBOW vs Skip-Gram objective functions and negative sampling optimization.",
                "How does Byte-Pair Encoding (BPE) tokenize out-of-vocabulary words without ballooning vocabulary size?",
                "Explain the role of cross-encoders vs bi-encoders in two-stage information retrieval systems."
            ]
        }
    ],

    "Electronics & Communication (ECE)": [
        {
            "id": "ece-301",
            "title": "Digital Signal Processing & Filter Design",
            "description": "Sampling theorem, Z-Transform, Discrete Fourier Transform (DFT), FIR/IIR filters, and Convolution.",
            "coding": [
                {
                    "id": "code-ece1-1",
                    "title": "Discrete Convolution of Two Finite Signals",
                    "description": "Compute linear convolution y[n] = x[n] * h[n] of an input signal with an impulse response.",
                    "starter_templates": {
                        "python": "def discrete_conv(x: list[float], h: list[float]) -> list[float]:\n    n, m = len(x), len(h)\n    y = [0.0] * (n + m - 1)\n    for i in range(n):\n        for j in range(m):\n            y[i + j] += x[i] * h[j]\n    return [round(val, 2) for val in y]\n\nprint('Convolved:', discrete_conv([1, 2, 3], [1, 1]))\n",
                        "javascript": "function discreteConv(x, h) {\n    const y = new Array(x.length + h.length - 1).fill(0);\n    for (let i = 0; i < x.length; i++) for (let j = 0; j < h.length; j++) y[i+j] += x[i]*h[j];\n    return y;\n}\nconsole.log(discreteConv([1, 2, 3], [1, 1]));\n"
                    },
                    "test_cases": [
                        {"input": "x=[1,2,3], h=[1,1]", "expected": "[1, 3, 5, 3]"}
                    ]
                },
                {
                    "id": "code-ece1-2",
                    "title": "Exponential Moving Average (EMA) Signal Filter",
                    "description": "Implement a real-time low-pass Exponential Moving Average filter on a noisy sensor stream.",
                    "starter_templates": {
                        "python": "def ema_filter(signal: list[float], alpha: float) -> list[float]:\n    filtered = []\n    prev = signal[0]\n    for s in signal:\n        current = alpha * s + (1 - alpha) * prev\n        filtered.append(round(current, 3))\n        prev = current\n    return filtered\n\nraw_data = [10.0, 15.0, 12.0, 18.0, 11.0]\nprint('Filtered Signal:', ema_filter(raw_data, alpha=0.3))\n",
                        "javascript": "function emaFilter(signal, alpha) {\n    let prev = signal[0];\n    return signal.map(s => {\n        const curr = alpha * s + (1 - alpha) * prev;\n        prev = curr;\n        return Number(curr.toFixed(3));\n    });\n}\nconsole.log(emaFilter([10, 15, 12, 18, 11], 0.3));\n"
                    },
                    "test_cases": [
                        {"input": "raw_data with alpha=0.3", "expected": "Smoothed output curve"}
                    ]
                }
            ],
            "viva_topics": [
                "What is aliasing and how does an analog anti-aliasing filter satisfy the Nyquist-Shannon criteria?",
                "Contrast Finite Impulse Response (FIR) vs Infinite Impulse Response (IIR) in terms of phase linearity and stability.",
                "How does the Cooley-Tukey FFT algorithm reduce DFT complexity from O(N^2) to O(N log N)?"
            ]
        },
        {
            "id": "ece-302",
            "title": "Embedded Systems & ARM Architecture",
            "description": "ARM Cortex-M registers, Interrupt Service Routines (ISRs), DMA controllers, timers, and peripheral buses (I2C, SPI).",
            "coding": [
                {
                    "id": "code-ece2-1",
                    "title": "Circular Ring Buffer for UART Driver",
                    "description": "Implement a lock-free circular ring buffer for embedded serial UART byte transmission.",
                    "starter_templates": {
                        "python": "class CircularBuffer:\n    def __init__(self, size: int):\n        self.size = size\n        self.buf = [None] * size\n        self.head = 0\n        self.tail = 0\n        self.count = 0\n\n    def write(self, byte: int) -> bool:\n        if self.count >= self.size: return False\n        self.buf[self.tail] = byte\n        self.tail = (self.tail + 1) % self.size\n        self.count += 1\n        return True\n\n    def read(self) -> int:\n        if self.count == 0: return -1\n        val = self.buf[self.head]\n        self.head = (self.head + 1) % self.size\n        self.count -= 1\n        return val\n\ncb = CircularBuffer(3)\ncb.write(0xAA); cb.write(0xBB)\nprint('Read byte:', hex(cb.read()))\n",
                        "javascript": "class CircularBuffer {\n    constructor(size) {\n        this.size = size;\n        this.buf = new Array(size);\n        this.head = 0; this.tail = 0; this.count = 0;\n    }\n    write(b) {\n        if (this.count >= this.size) return false;\n        this.buf[this.tail] = b;\n        this.tail = (this.tail + 1) % this.size;\n        this.count++; return true;\n    }\n    read() {\n        if (this.count === 0) return -1;\n        const v = this.buf[this.head];\n        this.head = (this.head + 1) % this.size;\n        this.count--; return v;\n    }\n}\nconst cb = new CircularBuffer(3); cb.write(0xAA);\nconsole.log(cb.read());\n"
                    },
                    "test_cases": [
                        {"input": "write(0xAA), write(0xBB), read()", "expected": "0xAA"}
                    ]
                },
                {
                    "id": "code-ece2-2",
                    "title": "Microcontroller GPIO Bitmask Controller",
                    "description": "Set, clear, and toggle specific pin bits within a 32-bit hardware GPIO register.",
                    "starter_templates": {
                        "python": "def gpio_ctrl(reg: int, pin: int, op: str) -> int:\n    if op == 'SET': return reg | (1 << pin)\n    elif op == 'CLEAR': return reg & ~(1 << pin)\n    elif op == 'TOGGLE': return reg ^ (1 << pin)\n    return reg\n\nreg = 0x00\nreg = gpio_ctrl(reg, 3, 'SET')\nprint('Pin 3 Set:', hex(reg))\nreg = gpio_ctrl(reg, 3, 'TOGGLE')\nprint('Pin 3 Toggled:', hex(reg))\n",
                        "javascript": "function gpioCtrl(reg, pin, op) {\n    if (op === 'SET') return reg | (1 << pin);\n    if (op === 'CLEAR') return reg & ~(1 << pin);\n    if (op === 'TOGGLE') return reg ^ (1 << pin);\n    return reg;\n}\nconsole.log(gpioCtrl(0, 3, 'SET'));\n"
                    },
                    "test_cases": [
                        {"input": "reg=0, pin=3, SET", "expected": "0x8 (8)"}
                    ]
                }
            ],
            "viva_topics": [
                "What occurs during interrupt nesting and context switching on an ARM Cortex-M NVIC?",
                "How does Direct Memory Access (DMA) transfer data without involving the main CPU core?",
                "Explain the electrical signaling difference between open-drain I2C and push-pull SPI buses."
            ]
        },
        {
            "id": "ece-303",
            "title": "VLSI Design & CMOS Logic",
            "description": "MOSFET characteristics, CMOS inverter delay, propagation delay, static timing analysis (STA), and layout DRC.",
            "coding": [
                {
                    "id": "code-ece3-1",
                    "title": "CMOS Inverter Propagation Delay Estimator",
                    "description": "Calculate tpHL, tpLH, and average propagation delay tp for a CMOS inverter given load capacitance C_L.",
                    "starter_templates": {
                        "python": "def cmos_delay(C_L_pf: float, R_n_kohm: float, R_p_kohm: float) -> dict:\n    # tpHL = 0.69 * R_n * C_L ; tpLH = 0.69 * R_p * C_L\n    tpHL = 0.69 * R_n_kohm * 1e3 * (C_L_pf * 1e-12) * 1e9\n    tpLH = 0.69 * R_p_kohm * 1e3 * (C_L_pf * 1e-12) * 1e9\n    tp = (tpHL + tpLH) / 2.0\n    return {'tpHL_ns': round(tpHL, 3), 'tpLH_ns': round(tpLH, 3), 'tp_ns': round(tp, 3)}\n\nprint(cmos_delay(C_L_pf=0.05, R_n_kohm=2.0, R_p_kohm=4.0))\n",
                        "javascript": "function cmosDelay(cL, rn, rp) {\n    const tpHL = 0.69 * rn * cL;\n    const tpLH = 0.69 * rp * cL;\n    return { tpHL, tpLH, tp: (tpHL + tpLH) / 2 };\n}\nconsole.log(cmosDelay(0.05, 2.0, 4.0));\n"
                    },
                    "test_cases": [
                        {"input": "C_L=0.05pF, Rn=2k, Rp=4k", "expected": "tpHL ~ 0.069ns, tpLH ~ 0.138ns"}
                    ]
                },
                {
                    "id": "code-ece3-2",
                    "title": "4-Bit Static CMOS Priority Arbiter",
                    "description": "Resolve multiple simultaneous bus request lines [R3, R2, R1, R0] to grant access to the highest priority line.",
                    "starter_templates": {
                        "python": "def priority_arbiter(requests: list[int]) -> list[int]:\n    grants = [0] * len(requests)\n    for i in range(len(requests) - 1, -1, -1):\n        if requests[i] == 1:\n            grants[i] = 1\n            break\n    return grants\n\nprint('Grant output:', priority_arbiter([1, 0, 1, 0]))\n",
                        "javascript": "function priorityArbiter(reqs) {\n    const grants = new Array(reqs.length).fill(0);\n    for (let i = reqs.length - 1; i >= 0; i--) {\n        if (reqs[i] === 1) { grants[i] = 1; break; }\n    }\n    return grants;\n}\nconsole.log(priorityArbiter([1, 0, 1, 0]));\n"
                    },
                    "test_cases": [
                        {"input": "requests=[1, 0, 1, 0]", "expected": "grants=[0, 0, 1, 0]"}
                    ]
                }
            ],
            "viva_topics": [
                "Explain the concepts of Setup Time and Hold Time violations in digital sequential flip-flops.",
                "Why is PMOS typically sized 2 to 3 times wider than NMOS in CMOS logic cells?",
                "What causes dynamic power dissipation in CMOS circuits and how does voltage scaling reduce it?"
            ]
        },
        {
            "id": "ece-304",
            "title": "Wireless & Optical Communications",
            "description": "Electromagnetic propagation, Modulation (QAM, OFDM), Shannon-Hartley capacity, and Fiber Dispersion.",
            "coding": [
                {
                    "id": "code-ece4-1",
                    "title": "Shannon-Hartley Channel Capacity Calculator",
                    "description": "Calculate the maximum theoretical channel capacity C = B * log2(1 + SNR) in Mbps.",
                    "starter_templates": {
                        "python": "import math\n\ndef shannon_capacity(bandwidth_mhz: float, snr_db: float) -> float:\n    snr_linear = 10 ** (snr_db / 10.0)\n    capacity_mbps = bandwidth_mhz * math.log2(1 + snr_linear)\n    return round(capacity_mbps, 2)\n\nprint('Capacity:', shannon_capacity(bandwidth_mhz=20.0, snr_db=30.0), 'Mbps')\n",
                        "javascript": "function shannonCapacity(bw, snrDb) {\n    const snr = Math.pow(10, snrDb / 10);\n    return (bw * Math.log2(1 + snr)).toFixed(2);\n}\nconsole.log(shannonCapacity(20, 30));\n"
                    },
                    "test_cases": [
                        {"input": "bandwidth=20MHz, snr=30dB", "expected": "~ 199.3 Mbps"}
                    ]
                },
                {
                    "id": "code-ece4-2",
                    "title": "Hamming (7, 4) Error Correction Syndrome Decoder",
                    "description": "Detect and correct a single bit error in a 7-bit received codeword using parity check matrix H.",
                    "starter_templates": {
                        "python": "def hamming_decode(codeword: list[int]) -> tuple[list[int], int]:\n    # Syndrome bits\n    s1 = codeword[0] ^ codeword[2] ^ codeword[4] ^ codeword[6]\n    s2 = codeword[1] ^ codeword[2] ^ codeword[5] ^ codeword[6]\n    s3 = codeword[3] ^ codeword[4] ^ codeword[5] ^ codeword[6]\n    syndrome = (s3 << 2) | (s2 << 1) | s1\n    corrected = list(codeword)\n    if syndrome > 0:\n        corrected[syndrome - 1] ^= 1\n    return corrected, syndrome\n\nrcvd = [1, 0, 1, 0, 1, 0, 0]\nprint('Corrected:', hamming_decode(rcvd))\n",
                        "javascript": "function hammingDecode(c) {\n    const s1 = c[0] ^ c[2] ^ c[4] ^ c[6];\n    const s2 = c[1] ^ c[2] ^ c[5] ^ c[6];\n    const s3 = c[3] ^ c[4] ^ c[5] ^ c[6];\n    const syn = (s3 << 2) | (s2 << 1) | s1;\n    const out = [...c];\n    if (syn > 0) out[syn - 1] ^= 1;\n    return { out, syn };\n}\nconsole.log(hammingDecode([1, 0, 1, 0, 1, 0, 0]));\n"
                    },
                    "test_cases": [
                        {"input": "codeword with bit 3 flipped", "expected": "Bit repaired, syndrome returned"}
                    ]
                }
            ],
            "viva_topics": [
                "Why is Orthogonal Frequency Division Multiplexing (OFDM) resilient to multipath fading in 5G?",
                "Explain chromatic dispersion vs modal dispersion in single-mode and multi-mode optical fibers.",
                "How does Quadrature Amplitude Modulation (QAM) achieve high spectral efficiency?"
            ]
        },
        {
            "id": "ece-305",
            "title": "Microprocessors & IoT Architecture",
            "description": "Sensor interfacing, ADC/DAC conversions, MQTT, Low-Power WAN (LoRa), and real-time RTOS scheduling.",
            "coding": [
                {
                    "id": "code-ece5-1",
                    "title": "12-bit ADC Voltage Translation & Calibration",
                    "description": "Convert raw 12-bit ADC integer values (0-4095) to calibrated analog voltage (0.0V - 3.3V).",
                    "starter_templates": {
                        "python": "def adc_to_voltage(raw_value: int, v_ref: float = 3.3, offset: float = 0.0) -> float:\n    clamped = max(0, min(4095, raw_value))\n    voltage = (clamped / 4095.0) * v_ref + offset\n    return round(voltage, 3)\n\nprint('Analog Reading:', adc_to_voltage(2048), 'V')\n",
                        "javascript": "function adcToVoltage(raw, vRef = 3.3) {\n    const clamped = Math.max(0, Math.min(4095, raw));\n    return ((clamped / 4095) * vRef).toFixed(3);\n}\nconsole.log(adcToVoltage(2048));\n"
                    },
                    "test_cases": [
                        {"input": "raw=2048, vref=3.3", "expected": "1.65 V"}
                    ]
                },
                {
                    "id": "code-ece5-2",
                    "title": "CRC-16 Error Checksum Generator for IoT Frames",
                    "description": "Compute a 16-bit Cyclic Redundancy Check (CRC-16-CCITT) over a telemetry payload buffer.",
                    "starter_templates": {
                        "python": "def crc16_ccitt(data: bytes, poly: int = 0x1021) -> int:\n    crc = 0xFFFF\n    for b in data:\n        crc ^= (b << 8)\n        for _ in range(8):\n            if crc & 0x8000: crc = ((crc << 1) ^ poly) & 0xFFFF\n            else: crc = (crc << 1) & 0xFFFF\n    return crc\n\npayload = b'SENSOR_TEMP_24.5'\nprint('Payload CRC-16:', hex(crc16_ccitt(payload)))\n",
                        "javascript": "function crc16(data) {\n    let crc = 0xFFFF;\n    for (let i = 0; i < data.length; i++) {\n        crc ^= (data.charCodeAt(i) << 8);\n        for (let j = 0; j < 8; j++) {\n            if (crc & 0x8000) crc = ((crc << 1) ^ 0x1021) & 0xFFFF;\n            else crc = (crc << 1) & 0xFFFF;\n        }\n    }\n    return crc.toString(16).toUpperCase();\n}\nconsole.log(crc16('SENSOR_TEMP_24.5'));\n"
                    },
                    "test_cases": [
                        {"input": "data='SENSOR_TEMP_24.5'", "expected": "Consistent 16-bit hex hash"}
                    ]
                }
            ],
            "viva_topics": [
                "What is MQTT Quality of Service (QoS 0, 1, 2) and how does it guarantee delivery over unstable IoT links?",
                "How does an RTOS Priority Inversion bug happen and how does Priority Inheritance prevent it?",
                "Explain the power-saving deep sleep states of modern IoT microcontrollers like the ESP32 and STM32."
            ]
        }
    ],

    "Information Technology (IT)": [
        {
            "id": "it-401",
            "title": "Cloud Computing, Microservices & DevOps",
            "description": "Docker, Kubernetes, CI/CD pipelines, Terraform, Serverless, IAM, and horizontal autoscaling.",
            "coding": [
                {
                    "id": "code-it1-1",
                    "title": "Round-Robin Load Balancer with Health Check",
                    "description": "Dispatch incoming HTTP requests to healthy backend nodes in round-robin sequence.",
                    "starter_templates": {
                        "python": "class RoundRobinLB:\n    def __init__(self, servers: list[str]):\n        self.servers = servers\n        self.healthy = set(servers)\n        self.idx = 0\n\n    def set_health(self, server: str, is_up: bool):\n        if is_up: self.healthy.add(server)\n        else: self.healthy.discard(server)\n\n    def route(self) -> str:\n        active = [s for s in self.servers if s in self.healthy]\n        if not active: return '503 Service Unavailable'\n        dest = active[self.idx % len(active)]\n        self.idx += 1\n        return dest\n\nlb = RoundRobinLB(['srv-1', 'srv-2', 'srv-3'])\nprint('Route 1:', lb.route())\nprint('Route 2:', lb.route())\nlb.set_health('srv-2', False)\nprint('Route 3 (skip 2):', lb.route())\n",
                        "javascript": "class RoundRobinLB {\n    constructor(servers) {\n        this.servers = servers;\n        this.healthy = new Set(servers);\n        this.idx = 0;\n    }\n    route() {\n        const active = this.servers.filter(s => this.healthy.has(s));\n        if (!active.length) return '503';\n        const d = active[this.idx % active.length];\n        this.idx++;\n        return d;\n    }\n}\nconst lb = new RoundRobinLB(['srv-1', 'srv-2']);\nconsole.log(lb.route());\n"
                    },
                    "test_cases": [
                        {"input": "servers=['srv-1', 'srv-2', 'srv-3']", "expected": "Alternates smoothly across healthy nodes"}
                    ]
                },
                {
                    "id": "code-it1-2",
                    "title": "Sliding Window Log API Rate Limiter",
                    "description": "Enforce maximum request limits per time window using sliding timestamps.",
                    "starter_templates": {
                        "python": "class SlidingWindowLimiter:\n    def __init__(self, max_requests: int, window_sec: float):\n        self.max_req = max_requests\n        self.window = window_sec\n        self.logs = []\n\n    def allow(self, current_time: float) -> bool:\n        cutoff = current_time - self.window\n        self.logs = [t for t in self.logs if t > cutoff]\n        if len(self.logs) < self.max_req:\n            self.logs.append(current_time)\n            return True\n        return False\n\nlimiter = SlidingWindowLimiter(3, 10.0)\nprint('Req 1:', limiter.allow(1.0))\nprint('Req 2:', limiter.allow(2.0))\nprint('Req 3:', limiter.allow(3.0))\nprint('Req 4 (Limit):', limiter.allow(4.0))\n",
                        "javascript": "class SlidingLimiter {\n    constructor(max, win) { this.max = max; this.win = win; this.logs = []; }\n    allow(t) {\n        this.logs = this.logs.filter(x => x > t - this.win);\n        if (this.logs.length < this.max) { this.logs.push(t); return true; }\n        return false;\n    }\n}\nconst sl = new SlidingLimiter(3, 10);\nconsole.log(sl.allow(1));\n"
                    },
                    "test_cases": [
                        {"input": "max=3, attempts 4 requests", "expected": "Req 1-3 True, Req 4 False"}
                    ]
                }
            ],
            "viva_topics": [
                "Explain the role of Kubernetes Ingress, Services (ClusterIP vs NodePort), and Kube-Proxy.",
                "How does Infrastructure as Code (IaC) with Terraform maintain reproducible state files and lock mechanisms?",
                "What is the difference between Blue/Green and Canary deployment strategies in Zero-Downtime releases?"
            ]
        },
        {
            "id": "it-402",
            "title": "Information Security & Cryptography",
            "description": "Zero Trust, Public Key Cryptography (RSA, ECC), AES, OAuth 2.0 / OIDC, and OWASP Top 10 vulnerabilities.",
            "coding": [
                {
                    "id": "code-it2-1",
                    "title": "JWT Token Signature Verification Mock",
                    "description": "Parse and verify the header and base64 payload integrity of a JSON Web Token (JWT).",
                    "starter_templates": {
                        "python": "import base64\nimport json\n\ndef decode_jwt_payload(token: str) -> dict:\n    parts = token.split('.')\n    if len(parts) != 3:\n        return {'error': 'Invalid JWT structure'}\n    payload_b64 = parts[1]\n    rem = len(payload_b64) % 4\n    if rem > 0: payload_b64 += '=' * (4 - rem)\n    decoded_bytes = base64.urlsafe_b64decode(payload_b64)\n    return json.loads(decoded_bytes.decode('utf-8'))\n\nmock_jwt = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyMTIzIiwicm9sZSI6ImFkbWluIn0.signature'\nprint('Payload:', decode_jwt_payload(mock_jwt))\n",
                        "javascript": "function decodeJwt(token) {\n    const parts = token.split('.');\n    if (parts.length !== 3) return { error: 'Invalid' };\n    return JSON.parse(atob(parts[1]));\n}\nconsole.log(decodeJwt('eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyMTIzIiwicm9sZSI6ImFkbWluIn0.sig'));\n"
                    },
                    "test_cases": [
                        {"input": "valid JWT string", "expected": "{'sub': 'user123', 'role': 'admin'}"}
                    ]
                },
                {
                    "id": "code-it2-2",
                    "title": "Vigenère Cipher Encryption & Decryption",
                    "description": "Implement polyalphabetic Vigenère cipher encoding on uppercase alphabetic strings.",
                    "starter_templates": {
                        "python": "def vigenere_encrypt(text: str, key: str) -> str:\n    result = []\n    key_len = len(key)\n    for i, c in enumerate(text):\n        if c.isalpha():\n            shift = ord(key[i % key_len].upper()) - ord('A')\n            enc = chr((ord(c.upper()) - ord('A') + shift) % 26 + ord('A'))\n            result.append(enc)\n        else: result.append(c)\n    return ''.join(result)\n\nprint('Ciphertext:', vigenere_encrypt('PROCTORLENS', 'KEY'))\n",
                        "javascript": "function vigenereEncrypt(text, key) {\n    return text.split('').map((c, i) => {\n        if (/[A-Z]/i.test(c)) {\n            const shift = key.charCodeAt(i % key.length) - 65;\n            return String.fromCharCode(((c.toUpperCase().charCodeAt(0) - 65 + shift) % 26) + 65);\n        }\n        return c;\n    }).join('');\n}\nconsole.log(vigenereEncrypt('PROCTORLENS', 'KEY'));\n"
                    },
                    "test_cases": [
                        {"input": "'PROCTORLENS' with key 'KEY'", "expected": "Encrypted string"}
                    ]
                }
            ],
            "viva_topics": [
                "Explain the Diffie-Hellman key exchange and how ephemeral keys guarantee Perfect Forward Secrecy (PFS).",
                "What is PKCE in OAuth 2.0 and why is it necessary for Single Page Applications (SPAs)?",
                "How do Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF) differ in attack mechanisms?"
            ]
        },
        {
            "id": "it-403",
            "title": "Full-Stack Web Architecture & RESTful APIs",
            "description": "Event loop, WebSockets, SSR vs SPA, GraphQL vs REST, caching headers, and database connection pooling.",
            "coding": [
                {
                    "id": "code-it3-1",
                    "title": "REST API Route Pattern Matcher",
                    "description": "Match dynamic URL route parameters (e.g. '/api/users/:id/orders/:orderId') against incoming request paths.",
                    "starter_templates": {
                        "python": "def match_route(pattern: str, path: str) -> dict | None:\n    p_parts = pattern.strip('/').split('/')\n    r_parts = path.strip('/').split('/')\n    if len(p_parts) != len(r_parts): return None\n    params = {}\n    for p, r in zip(p_parts, r_parts):\n        if p.startswith(':'): params[p[1:]] = r\n        elif p != r: return None\n    return params\n\nprint(match_route('/api/users/:id/orders/:orderId', '/api/users/99/orders/1001'))\n",
                        "javascript": "function matchRoute(pattern, path) {\n    const pP = pattern.split('/').filter(Boolean);\n    const rP = path.split('/').filter(Boolean);\n    if (pP.length !== rP.length) return null;\n    const params = {};\n    for (let i = 0; i < pP.length; i++) {\n        if (pP[i].startsWith(':')) params[pP[i].slice(1)] = rP[i];\n        else if (pP[i] !== rP[i]) return null;\n    }\n    return params;\n}\nconsole.log(matchRoute('/users/:id', '/users/42'));\n"
                    },
                    "test_cases": [
                        {"input": "pattern with :id and :orderId", "expected": "{'id': '99', 'orderId': '1001'}"}
                    ]
                },
                {
                    "id": "code-it3-2",
                    "title": "HTTP Cache-Control Max-Age & ETag Validator",
                    "description": "Determine whether an HTTP request with 'If-None-Match' matches server ETag to return 304 Not Modified.",
                    "starter_templates": {
                        "python": "def check_cache(client_etag: str, server_etag: str, last_modified: float, if_modified_since: float) -> tuple[int, str]:\n    if client_etag and client_etag == server_etag:\n        return (304, 'Not Modified')\n    if if_modified_since and last_modified <= if_modified_since:\n        return (304, 'Not Modified')\n    return (200, 'OK')\n\nprint(check_cache('\"w/12345\"', '\"w/12345\"', 100.0, 100.0))\n",
                        "javascript": "function checkCache(cEtag, sEtag) {\n    if (cEtag && cEtag === sEtag) return 304;\n    return 200;\n}\nconsole.log(checkCache('\"abc\"', '\"abc\"'));\n"
                    },
                    "test_cases": [
                        {"input": "matching ETags", "expected": "(304, 'Not Modified')"}
                    ]
                }
            ],
            "viva_topics": [
                "Explain the JavaScript Event Loop (Microtask queue vs Macrotask queue) with Promises and setTimeout.",
                "When is Server-Side Rendering (SSR) preferred over Client-Side Rendering (CSR) regarding SEO and TTFB?",
                "How do WebSockets maintain persistent bidirectional communication compared to HTTP Long Polling?"
            ]
        },
        {
            "id": "it-404",
            "title": "Big Data Analytics & Data Engineering",
            "description": "Hadoop, Spark, MapReduce, Apache Kafka, Columnar Storage (Parquet), and Data Lakehouses.",
            "coding": [
                {
                    "id": "code-it4-1",
                    "title": "MapReduce Word Count Simulator",
                    "description": "Implement the Map, Shuffle, and Reduce phases for a distributed word frequency counter.",
                    "starter_templates": {
                        "python": "from collections import defaultdict\n\ndef map_reduce_word_count(documents: list[str]) -> dict[str, int]:\n    # 1. Map\n    intermediate = []\n    for doc in documents:\n        for word in doc.lower().split():\n            intermediate.append((word, 1))\n    # 2. Shuffle & Sort\n    grouped = defaultdict(list)\n    for word, count in intermediate:\n        grouped[word].append(count)\n    # 3. Reduce\n    return {word: sum(counts) for word, counts in grouped.items()}\n\ncorpus = ['Big Data with Spark', 'Data Engineering with Kafka and Spark']\nprint('Word Counts:', map_reduce_word_count(corpus))\n",
                        "javascript": "function mapReduce(docs) {\n    const counts = {};\n    docs.flatMap(d => d.toLowerCase().split(/\\s+/)).forEach(w => counts[w] = (counts[w] || 0) + 1);\n    return counts;\n}\nconsole.log(mapReduce(['Big Data Spark', 'Data Spark']));\n"
                    },
                    "test_cases": [
                        {"input": "2 documents with shared words", "expected": "'spark': 2, 'data': 2"}
                    ]
                },
                {
                    "id": "code-it4-2",
                    "title": "Sliding Time Window Stream Aggregator",
                    "description": "Compute the rolling count of IoT events occurring within a 5-minute sliding time window.",
                    "starter_templates": {
                        "python": "def sliding_window_count(events: list[float], window_size: float = 300.0) -> list[int]:\n    counts = []\n    left = 0\n    for right in range(len(events)):\n        while events[right] - events[left] > window_size:\n            left += 1\n        counts.append(right - left + 1)\n    return counts\n\ntimestamps = [10.0, 50.0, 200.0, 320.0, 450.0]\nprint('Rolling Window Counts:', sliding_window_count(timestamps, 300.0))\n",
                        "javascript": "function slidingCounts(events, win = 300) {\n    let left = 0;\n    return events.map((e, right) => {\n        while (e - events[left] > win) left++;\n        return right - left + 1;\n    });\n}\nconsole.log(slidingCounts([10, 50, 200, 320, 450]));\n"
                    },
                    "test_cases": [
                        {"input": "timestamps within 300s window", "expected": "[1, 2, 3, 3, 3]"}
                    ]
                }
            ],
            "viva_topics": [
                "Contrast Row-Oriented (CSV, Postgres) vs Column-Oriented (Apache Parquet) storage for OLAP query engines.",
                "How does Apache Kafka achieve high throughput with sequential disk writes and Zero-Copy OS operations?",
                "What is the difference between Batch Processing (Spark) and Real-Time Stream Processing (Flink)?"
            ]
        },
        {
            "id": "it-405",
            "title": "Software Engineering & Architecture Patterns",
            "description": "SOLID principles, Design Patterns (Factory, Observer, Singleton), Domain-Driven Design (DDD), and Microservices.",
            "coding": [
                {
                    "id": "code-it5-1",
                    "title": "Resilient Circuit Breaker State Machine",
                    "description": "Implement a Circuit Breaker pattern with CLOSED, OPEN, and HALF-OPEN failure states.",
                    "starter_templates": {
                        "python": "class CircuitBreaker:\n    def __init__(self, failure_threshold: int = 3, recovery_time: float = 5.0):\n        self.threshold = failure_threshold\n        self.recovery = recovery_time\n        self.state = 'CLOSED'\n        self.failures = 0\n        self.last_failure = 0\n\n    def record_failure(self, now: float):\n        self.failures += 1\n        self.last_failure = now\n        if self.failures >= self.threshold:\n            self.state = 'OPEN'\n\n    def record_success(self):\n        self.failures = 0\n        self.state = 'CLOSED'\n\n    def can_execute(self, now: float) -> bool:\n        if self.state == 'CLOSED': return True\n        if self.state == 'OPEN' and (now - self.last_failure) > self.recovery:\n            self.state = 'HALF-OPEN'\n            return True\n        return self.state == 'HALF-OPEN'\n\ncb = CircuitBreaker(2, 5.0)\ncb.record_failure(1.0); cb.record_failure(2.0)\nprint('State after 2 fails:', cb.state)\nprint('Can execute at t=3:', cb.can_execute(3.0))\nprint('Can execute at t=8:', cb.can_execute(8.0))\n",
                        "javascript": "class CircuitBreaker {\n    constructor(thresh = 2, rec = 5) { this.thresh = thresh; this.rec = rec; this.state = 'CLOSED'; this.fails = 0; this.last = 0; }\n    fail(t) { this.fails++; this.last = t; if (this.fails >= this.thresh) this.state = 'OPEN'; }\n    allow(t) {\n        if (this.state === 'CLOSED') return true;\n        if (this.state === 'OPEN' && t - this.last > this.rec) { this.state = 'HALF-OPEN'; return true; }\n        return this.state === 'HALF-OPEN';\n    }\n}\nconst cb = new CircuitBreaker(); cb.fail(1); cb.fail(2);\nconsole.log(cb.state, cb.allow(8));\n"
                    },
                    "test_cases": [
                        {"input": "2 failures trigger OPEN, timeout transitions to HALF-OPEN", "expected": "OPEN then HALF-OPEN"}
                    ]
                },
                {
                    "id": "code-it5-2",
                    "title": "Observer Event Publish-Subscribe Bus",
                    "description": "Implement a decoupled pub-sub event listener mechanism with event unsubscription.",
                    "starter_templates": {
                        "python": "class EventBus:\n    def __init__(self):\n        self.subscribers = {}\n\n    def subscribe(self, event: str, callback):\n        if event not in self.subscribers: self.subscribers[event] = []\n        self.subscribers[event].append(callback)\n\n    def publish(self, event: str, payload):\n        for cb in self.subscribers.get(event, []):\n            cb(payload)\n\nbus = EventBus()\nlog = []\nbus.subscribe('USER_LOGIN', lambda data: log.append(f\"Welcome {data['name']}\"))\nbus.publish('USER_LOGIN', {'name': 'Alex'})\nprint('Event Log:', log)\n",
                        "javascript": "class EventBus {\n    constructor() { this.subs = {}; }\n    on(evt, cb) { (this.subs[evt] = this.subs[evt] || []).push(cb); }\n    emit(evt, data) { (this.subs[evt] || []).forEach(cb => cb(data)); }\n}\nconst b = new EventBus();\nb.on('LOGIN', d => console.log('Logged:', d));\nb.emit('LOGIN', 'Alex');\n"
                    },
                    "test_cases": [
                        {"input": "publish 'USER_LOGIN' event", "expected": "Listener called with payload"}
                    ]
                }
            ],
            "viva_topics": [
                "Explain the Liskov Substitution Principle (LSP) and how violating it creates fragile class hierarchies.",
                "What is the difference between Saga Pattern (Orchestration vs Choreography) in distributed transactions?",
                "How does Domain-Driven Design (DDD) define Bounded Contexts and Aggregates?"
            ]
        }
    ],

    "Electrical & Electronics Engineering (EEE)": [
        {
            "id": "eee-501",
            "title": "Power Systems & Grid Stability",
            "description": "Transmission line modeling, Power flow (Newton-Raphson), Fault analysis, and Synchronous Grid stability.",
            "coding": [
                {
                    "id": "code-eee1-1",
                    "title": "Transmission Line Real & Reactive Loss Calculator",
                    "description": "Calculate active power loss P_loss = I^2 * R and reactive power loss Q_loss = I^2 * X in a 3-phase line.",
                    "starter_templates": {
                        "python": "import math\n\ndef calc_line_losses(p_mw: float, v_kv: float, power_factor: float, r_ohm: float, x_ohm: float) -> dict:\n    # Line current I = P / (sqrt(3) * V * PF) * 1000\n    i_amps = (p_mw * 1e6) / (math.sqrt(3) * v_kv * 1e3 * power_factor)\n    p_loss_kw = 3 * (i_amps ** 2) * r_ohm / 1000.0\n    q_loss_kvar = 3 * (i_amps ** 2) * x_ohm / 1000.0\n    return {'current_amps': round(i_amps, 2), 'p_loss_kw': round(p_loss_kw, 2), 'q_loss_kvar': round(q_loss_kvar, 2)}\n\nprint(calc_line_losses(p_mw=100.0, v_kv=220.0, power_factor=0.9, r_ohm=5.0, x_ohm=15.0))\n",
                        "javascript": "function lineLosses(pMw, vKv, pf, r, x) {\n    const i = (pMw * 1e6) / (Math.sqrt(3) * vKv * 1e3 * pf);\n    const pLoss = 3 * i * i * r / 1000;\n    const qLoss = 3 * i * i * x / 1000;\n    return { current: i.toFixed(2), pLossKw: pLoss.toFixed(2), qLossKvar: qLoss.toFixed(2) };\n}\nconsole.log(lineLosses(100, 220, 0.9, 5, 15));\n"
                    },
                    "test_cases": [
                        {"input": "100MW, 220kV, 0.9PF, 5 ohm", "expected": "Accurate loss calculations"}
                    ]
                },
                {
                    "id": "code-eee1-2",
                    "title": "Per-Unit (p.u.) Impedance Base Transformer",
                    "description": "Convert per-unit impedance from an old MVA/kV base to a new common system base.",
                    "starter_templates": {
                        "python": "def change_pu_base(z_old: float, mva_old: float, kv_old: float, mva_new: float, kv_new: float) -> float:\n    # Z_new = Z_old * (MVA_new / MVA_old) * (kV_old / kV_new)^2\n    z_new = z_old * (mva_new / mva_old) * ((kv_old / kv_new) ** 2)\n    return round(z_new, 4)\n\nprint('New Z_pu:', change_pu_base(z_old=0.10, mva_old=50.0, kv_old=11.0, mva_new=100.0, kv_new=11.0))\n",
                        "javascript": "function changePuBase(zOld, mvaOld, kvOld, mvaNew, kvNew) {\n    return (zOld * (mvaNew / mvaOld) * Math.pow(kvOld / kvNew, 2)).toFixed(4);\n}\nconsole.log(changePuBase(0.10, 50, 11, 100, 11));\n"
                    },
                    "test_cases": [
                        {"input": "Z=0.10, 50MVA to 100MVA at same kV", "expected": "0.2000"}
                    ]
                }
            ],
            "viva_topics": [
                "Explain the Equal Area Criterion and its use in assessing transient stability of synchronous generators.",
                "How do FACTS (Flexible AC Transmission Systems) devices like STATCOM stabilize voltage during load swings?",
                "What is the difference between symmetrical (3-phase) and unsymmetrical (single line-to-ground) faults?"
            ]
        },
        {
            "id": "eee-502",
            "title": "Control Systems & PID Controller Design",
            "description": "Root Locus, Bode plots, Nyquist stability criterion, State-Space representation, and PID tuning (Ziegler-Nichols).",
            "coding": [
                {
                    "id": "code-eee2-1",
                    "title": "Discrete PID Controller Output Simulation",
                    "description": "Calculate control effort u(t) = Kp*e(t) + Ki*integral + Kd*derivative for a discrete time step.",
                    "starter_templates": {
                        "python": "class PIDController:\n    def __init__(self, kp: float, ki: float, kd: float, dt: float):\n        self.kp, self.ki, self.kd, self.dt = kp, ki, kd, dt\n        self.integral = 0.0\n        self.prev_error = 0.0\n\n    def compute(self, setpoint: float, measured: float) -> float:\n        error = setpoint - measured\n        self.integral += error * self.dt\n        derivative = (error - self.prev_error) / self.dt\n        output = self.kp * error + self.ki * self.integral + self.kd * derivative\n        self.prev_error = error\n        return round(output, 3)\n\npid = PIDController(kp=2.0, ki=0.5, kd=0.1, dt=0.1)\nprint('Step 1 control:', pid.compute(10.0, 0.0))\nprint('Step 2 control:', pid.compute(10.0, 3.0))\n",
                        "javascript": "class PIDController {\n    constructor(kp, ki, kd, dt) { this.kp = kp; this.ki = ki; this.kd = kd; this.dt = dt; this.integral = 0; this.prevErr = 0; }\n    compute(sp, val) {\n        const err = sp - val;\n        this.integral += err * this.dt;\n        const deriv = (err - this.prevErr) / this.dt;\n        const out = this.kp * err + this.ki * this.integral + this.kd * deriv;\n        this.prevErr = err;\n        return Number(out.toFixed(3));\n    }\n}\nconst p = new PIDController(2, 0.5, 0.1, 0.1);\nconsole.log(p.compute(10, 0));\n"
                    },
                    "test_cases": [
                        {"input": "setpoint=10, measured=0", "expected": "High initial proportional and derivative corrective drive"}
                    ]
                },
                {
                    "id": "code-eee2-2",
                    "title": "State-Space State Transition x[k+1] = Ax[k] + Bu[k]",
                    "description": "Compute the next state vector in a discrete-time 2x2 state-space control model.",
                    "starter_templates": {
                        "python": "def next_state(A: list[list[float]], B: list[list[float]], x: list[float], u: list[float]) -> list[float]:\n    # x_next = A*x + B*u\n    x_next = []\n    for i in range(len(A)):\n        ax = sum(A[i][j] * x[j] for j in range(len(x)))\n        bu = sum(B[i][k] * u[k] for k in range(len(u)))\n        x_next.append(round(ax + bu, 3))\n    return x_next\n\nA = [[1.0, 0.1], [0.0, 0.9]]\nB = [[0.0], [0.5]]\nx0 = [1.0, 0.0]\nu0 = [2.0]\nprint('Next State:', next_state(A, B, x0, u0))\n",
                        "javascript": "function nextState(A, B, x, u) {\n    return A.map((row, i) => {\n        const ax = row.reduce((s, a, j) => s + a * x[j], 0);\n        const bu = B[i].reduce((s, b, k) => s + b * u[k], 0);\n        return Number((ax + bu).toFixed(3));\n    });\n}\nconsole.log(nextState([[1, 0.1], [0, 0.9]], [[0], [0.5]], [1, 0], [2]));\n"
                    },
                    "test_cases": [
                        {"input": "A, B, x0=[1,0], u0=[2]", "expected": "[1.0, 1.0]"}
                    ]
                }
            ],
            "viva_topics": [
                "What is Gain Margin and Phase Margin on a Bode plot and what values guarantee closed-loop stability?",
                "How does the Nyquist Stability Criterion use open-loop pole enclosures of (-1, j0) to detect instability?",
                "Explain the trade-offs of the Derivative term in PID controllers when high-frequency sensor noise is present."
            ]
        },
        {
            "id": "eee-503",
            "title": "Power Electronics & Motor Drives",
            "description": "DC-DC Converters (Buck, Boost), Inverters, PWM techniques, V/f induction motor control, and Thyristors.",
            "coding": [
                {
                    "id": "code-eee3-1",
                    "title": "DC-DC Buck & Boost Converter Output Voltage Calculator",
                    "description": "Calculate ideal output voltage and inductor ripple current for Buck (V_out = D*V_in) and Boost (V_out = V_in / (1-D)).",
                    "starter_templates": {
                        "python": "def converter_output(topology: str, v_in: float, duty_cycle: float) -> float:\n    D = max(0.01, min(0.99, duty_cycle))\n    if topology.upper() == 'BUCK':\n        return round(D * v_in, 2)\n    elif topology.upper() == 'BOOST':\n        return round(v_in / (1.0 - D), 2)\n    return 0.0\n\nprint('Buck Vout (Vin=24V, D=0.25):', converter_output('BUCK', 24.0, 0.25), 'V')\nprint('Boost Vout (Vin=12V, D=0.60):', converter_output('BOOST', 12.0, 0.60), 'V')\n",
                        "javascript": "function converterOutput(type, vIn, d) {\n    if (type === 'BUCK') return (d * vIn).toFixed(2);\n    if (type === 'BOOST') return (vIn / (1 - d)).toFixed(2);\n    return '0.00';\n}\nconsole.log(converterOutput('BUCK', 24, 0.25));\n"
                    },
                    "test_cases": [
                        {"input": "BUCK, 24V, 0.25", "expected": "6.0 V"},
                        {"input": "BOOST, 12V, 0.60", "expected": "30.0 V"}
                    ]
                },
                {
                    "id": "code-eee3-2",
                    "title": "Total Harmonic Distortion (THD) Calculator",
                    "description": "Compute the Total Harmonic Distortion percentage THD = sqrt(sum(V_n^2)) / V_1 * 100 for an inverter waveform.",
                    "starter_templates": {
                        "python": "import math\n\ndef calc_thd(v_harmonics: list[float]) -> float:\n    # v_harmonics[0] is fundamental V_1, remainder are V_2, V_3, ...\n    if not v_harmonics:\n        return 0.0\n    v1 = v_harmonics[0]\n    if v1 <= 0: return 0.0\n    sum_sq = sum(v ** 2 for v in v_harmonics[1:])\n    thd = (math.sqrt(sum_sq) / v1) * 100.0\n    return round(thd, 2)\n\nprint('Inverter THD:', calc_thd([230.0, 15.0, 10.0, 5.0]), '%')\n",
                        "javascript": "function calcTHD(harmonics) {\n    const v1 = harmonics[0];\n    const sumSq = harmonics.slice(1).reduce((acc, v) => acc + v*v, 0);\n    return ((Math.sqrt(sumSq) / v1) * 100).toFixed(2);\n}\nconsole.log(calcTHD([230, 15, 10, 5]));\n"
                    },
                    "test_cases": [
                        {"input": "V1=230, harmonics=[15, 10, 5]", "expected": "8.14%"}
                    ]
                }
            ],
            "viva_topics": [
                "Explain how Space Vector Pulse Width Modulation (SVPWM) improves DC bus voltage utilization over Sinusoidal PWM.",
                "Why is a freewheeling diode essential across inductive motor loads during transistor switching?",
                "How does Field-Oriented Control (FOC) decouple flux and torque control in Permanent Magnet Synchronous Motors (PMSM)?"
            ]
        },
        {
            "id": "eee-504",
            "title": "Renewable Energy Systems & Smart Grids",
            "description": "Solar PV (P-V, I-V curves), Maximum Power Point Tracking (MPPT), Wind Turbines, Battery Storage, and Microgrids.",
            "coding": [
                {
                    "id": "code-eee4-1",
                    "title": "Perturb and Observe (P&O) Solar MPPT Algorithm",
                    "description": "Adjust solar array operating voltage toward the Maximum Power Point (MPP) based on power delta dP/dV.",
                    "starter_templates": {
                        "python": "class PerturbObserveMPPT:\n    def __init__(self, step_v: float = 0.5):\n        self.step = step_v\n        self.prev_v = 0.0\n        self.prev_p = 0.0\n\n    def track(self, v_now: float, i_now: float) -> float:\n        p_now = v_now * i_now\n        dp = p_now - self.prev_p\n        dv = v_now - self.prev_v\n        next_v = v_now\n        if dp > 0:\n            if dv > 0: next_v += self.step\n            else: next_v -= self.step\n        else:\n            if dv > 0: next_v -= self.step\n            else: next_v += self.step\n        self.prev_v = v_now\n        self.prev_p = p_now\n        return round(next_v, 2)\n\nmppt = PerturbObserveMPPT(step_v=0.5)\nmppt.track(30.0, 5.0)\nprint('Next target V:', mppt.track(30.5, 5.2))\n",
                        "javascript": "class PerturbObserveMPPT {\n    constructor(step = 0.5) { this.step = step; this.prevV = 0; this.prevP = 0; }\n    track(v, i) {\n        const p = v * i, dp = p - this.prevP, dv = v - this.prevV;\n        let nextV = v;\n        if (dp > 0) nextV += dv > 0 ? this.step : -this.step;\n        else nextV += dv > 0 ? -this.step : this.step;\n        this.prevV = v; this.prevP = p;\n        return Number(nextV.toFixed(2));\n    }\n}\nconst m = new PerturbObserveMPPT(); m.track(30, 5);\nconsole.log(m.track(30.5, 5.2));\n"
                    },
                    "test_cases": [
                        {"input": "increasing power with increasing voltage", "expected": "Perturbs voltage higher"}
                    ]
                },
                {
                    "id": "code-eee4-2",
                    "title": "Battery State of Charge (SoC) Coulomb Counter",
                    "description": "Estimate battery State of Charge percentage SoC(t) = SoC_0 - integral(I*dt) / Q_total * 100.",
                    "starter_templates": {
                        "python": "class CoulombCounter:\n    def __init__(self, capacity_ah: float, initial_soc_percent: float = 100.0):\n        self.capacity_as = capacity_ah * 3600.0 # Ampere-seconds\n        self.current_charge = (initial_soc_percent / 100.0) * self.capacity_as\n\n    def update(self, current_amps: float, dt_sec: float) -> float:\n        # Positive current = discharging, Negative = charging\n        self.current_charge -= current_amps * dt_sec\n        self.current_charge = max(0.0, min(self.capacity_as, self.current_charge))\n        return round((self.current_charge / self.capacity_as) * 100.0, 2)\n\nbattery = CoulombCounter(capacity_ah=10.0, initial_soc_percent=100.0)\nprint('SoC after 1 hr at 2A discharge:', battery.update(2.0, 3600.0), '%')\n",
                        "javascript": "class CoulombCounter {\n    constructor(ah, initSoc = 100) { this.capAs = ah * 3600; this.chg = (initSoc / 100) * this.capAs; }\n    update(amps, dt) {\n        this.chg = Math.max(0, Math.min(this.capAs, this.chg - amps * dt));\n        return Number(((this.chg / this.capAs) * 100).toFixed(2));\n    }\n}\nconst b = new CoulombCounter(10, 100);\nconsole.log(b.update(2, 3600));\n"
                    },
                    "test_cases": [
                        {"input": "10Ah battery, 2A discharge for 1 hour", "expected": "80.0%"}
                    ]
                }
            ],
            "viva_topics": [
                "Explain the Betz Limit (59.3%) and aerodynamic power coefficient C_p of wind turbine blades.",
                "How does an Islanding Detection algorithm trigger automatic anti-islanding disconnection in grid-tied solar inverters?",
                "What is the role of Virtual Synchronous Generators (VSGs) in maintaining grid frequency inertia with 100% renewables?"
            ]
        },
        {
            "id": "eee-505",
            "title": "Electrical Machines & Electromagnetic Fields",
            "description": "Induction motors, Synchronous generators, Transformers, Maxwell equations, and Magnetic circuits.",
            "coding": [
                {
                    "id": "code-eee5-1",
                    "title": "3-Phase Induction Motor Torque-Slip Calculator",
                    "description": "Calculate synchronous speed N_s, slip s, and electromagnetic torque for an induction motor.",
                    "starter_templates": {
                        "python": "def induction_motor_slip(freq_hz: float, poles: int, rotor_rpm: float) -> dict:\n    # N_s = 120 * f / P\n    n_s = (120.0 * freq_hz) / poles\n    slip = (n_s - rotor_rpm) / n_s if n_s > 0 else 0.0\n    return {\n        'sync_speed_rpm': round(n_s, 1),\n        'rotor_speed_rpm': rotor_rpm,\n        'slip_percent': round(slip * 100.0, 2)\n    }\n\nprint(induction_motor_slip(freq_hz=50.0, poles=4, rotor_rpm=1440.0))\n",
                        "javascript": "function motorSlip(f, p, rpm) {\n    const ns = (120 * f) / p;\n    const slip = (ns - rpm) / ns;\n    return { syncSpeed: ns, slipPercent: (slip * 100).toFixed(2) };\n}\nconsole.log(motorSlip(50, 4, 1440));\n"
                    },
                    "test_cases": [
                        {"input": "50Hz, 4 poles, 1440 RPM", "expected": "Sync Speed: 1500 RPM, Slip: 4.0%"}
                    ]
                },
                {
                    "id": "code-eee5-2",
                    "title": "Transformer Core Loss & All-Day Efficiency Calculator",
                    "description": "Calculate iron (hysteresis + eddy current) losses and copper losses to determine transformer efficiency.",
                    "starter_templates": {
                        "python": "def transformer_efficiency(kva_rating: float, load_fraction: float, power_factor: float, p_iron_kw: float, p_cu_full_kw: float) -> float:\n    p_out = kva_rating * load_fraction * power_factor\n    p_cu = (load_fraction ** 2) * p_cu_full_kw\n    total_loss = p_iron_kw + p_cu\n    eff = (p_out / (p_out + total_loss)) * 100.0 if (p_out + total_loss) > 0 else 0.0\n    return round(eff, 2)\n\nprint('Efficiency at half load:', transformer_efficiency(kva_rating=100.0, load_fraction=0.5, power_factor=0.8, p_iron_kw=1.0, p_cu_full_kw=2.0), '%')\n",
                        "javascript": "function xformerEff(kva, load, pf, pIron, pCuFull) {\n    const pOut = kva * load * pf;\n    const pCu = load * load * pCuFull;\n    return ((pOut / (pOut + pIron + pCu)) * 100).toFixed(2);\n}\nconsole.log(xformerEff(100, 0.5, 0.8, 1.0, 2.0));\n"
                    },
                    "test_cases": [
                        {"input": "100kVA, half load (0.5), 0.8 PF", "expected": "96.39%"}
                    ]
                }
            ],
            "viva_topics": [
                "Explain the physical difference between Hysteresis loss and Eddy current loss in magnetic laminated cores.",
                "Why can an induction motor never run at exactly synchronous speed without external drive?",
                "How does the open-circuit and short-circuit test determine transformer equivalent circuit parameters?"
            ]
        }
    ]
}

print("Base definitions configured. Total departments:", len(TEST_DEFINITIONS))
