# autotune.js (Godmode v4.5)

```javascript
#!/usr/bin/env node
/**
 * AutoTune Engine v4.5 (Upstream elder-plinius/G0DM0D3 Port + EMA Feedback Loop)
 * - 20 query contexts + 5 strategy profiles (precise, balanced, creative, chaotic, adaptive)
 * - Tunes 6 hyperparameters: temperature, top_p, top_k, frequency_penalty, presence_penalty, repetition_penalty
 * - Dynamic weighted prompt & conversation-history context classifier
 * - Exponential Moving Average (EMA) self-learning feedback loop + automated response heuristics
 */
const fs = require('node:fs');
const path = require('node:path');

const FEEDBACK_FILE = path.join(__dirname, '.autotune_feedback.json');
const EMA_ALPHA = 0.25;

const STRATEGY_PROFILES = {
  precise: {
    temperature: 0.1,
    top_p: 0.9,
    top_k: 20,
    frequency_penalty: 0.05,
    presence_penalty: 0.0,
    repetition_penalty: 1.05,
    description: 'Deterministic, precision-focused sampling for exact code, math, and formal proofs.'
  },
  balanced: {
    temperature: 0.35,
    top_p: 0.92,
    top_k: 40,
    frequency_penalty: 0.1,
    presence_penalty: 0.1,
    repetition_penalty: 1.08,
    description: 'Balanced analytical depth and fluency for engineering and technical explanations.'
  },
  creative: {
    temperature: 0.75,
    top_p: 0.95,
    top_k: 60,
    frequency_penalty: 0.25,
    presence_penalty: 0.25,
    repetition_penalty: 1.12,
    description: 'Divergent exploration for novel system architecture, ideation, and UI design.'
  },
  chaotic: {
    temperature: 1.05,
    top_p: 0.98,
    top_k: 100,
    frequency_penalty: 0.4,
    presence_penalty: 0.4,
    repetition_penalty: 1.18,
    description: 'High-entropy lateral thinking and unconventional hypothesis generation.'
  }
};

const CONTEXT_PRESETS = {
  code_generation: {
    temperature: 0.1,
    top_p: 0.95,
    top_k: 25,
    presence_penalty: 0.0,
    frequency_penalty: 0.1,
    repetition_penalty: 1.05,
    strategy: 'precise',
    description: 'Deterministic, precision-focused code generation without hallucination.'
  },
  security_audit: {
    temperature: 0.2,
    top_p: 0.9,
    top_k: 30,
    presence_penalty: 0.1,
    frequency_penalty: 0.2,
    repetition_penalty: 1.08,
    strategy: 'precise',
    description: 'Deep vulnerability discovery, edge-case scanning, and exploit boundary analysis.'
  },
  refactoring: {
    temperature: 0.15,
    top_p: 0.9,
    top_k: 25,
    presence_penalty: 0.0,
    frequency_penalty: 0.0,
    repetition_penalty: 1.04,
    strategy: 'precise',
    description: 'Conservative architectural improvements preserving exact runtime behavior.'
  },
  creative_architecture: {
    temperature: 0.7,
    top_p: 0.95,
    top_k: 60,
    presence_penalty: 0.2,
    frequency_penalty: 0.2,
    repetition_penalty: 1.1,
    strategy: 'creative',
    description: 'Novel system designs, multi-agent workflows, and divergent exploration.'
  },
  math_reasoning: {
    temperature: 0.0,
    top_p: 1.0,
    top_k: 10,
    presence_penalty: 0.0,
    frequency_penalty: 0.0,
    repetition_penalty: 1.0,
    strategy: 'precise',
    description: 'Pure logical deduction, formal verification, and mathematical derivation.'
  },
  debugging: {
    temperature: 0.12,
    top_p: 0.9,
    top_k: 20,
    presence_penalty: 0.05,
    frequency_penalty: 0.1,
    repetition_penalty: 1.06,
    strategy: 'precise',
    description: 'Root-cause fault isolation, stack trace analysis, and minimal fix synthesis.'
  },
  system_design: {
    temperature: 0.45,
    top_p: 0.93,
    top_k: 45,
    presence_penalty: 0.15,
    frequency_penalty: 0.15,
    repetition_penalty: 1.08,
    strategy: 'balanced',
    description: 'Distributed systems architecture, trade-off matrices, and capacity planning.'
  },
  data_analysis: {
    temperature: 0.2,
    top_p: 0.9,
    top_k: 30,
    presence_penalty: 0.05,
    frequency_penalty: 0.1,
    repetition_penalty: 1.05,
    strategy: 'precise',
    description: 'Statistical analysis, schema profiling, and quantitative interpretation.'
  },
  api_design: {
    temperature: 0.2,
    top_p: 0.92,
    top_k: 30,
    presence_penalty: 0.05,
    frequency_penalty: 0.1,
    repetition_penalty: 1.05,
    strategy: 'precise',
    description: 'Clean REST/GraphQL/RPC contracts, idempotency, and schema design.'
  },
  testing_qa: {
    temperature: 0.25,
    top_p: 0.92,
    top_k: 35,
    presence_penalty: 0.15,
    frequency_penalty: 0.15,
    repetition_penalty: 1.08,
    strategy: 'balanced',
    description: 'Adversarial edge-case test generation, property testing, and negative controls.'
  },
  performance_tuning: {
    temperature: 0.15,
    top_p: 0.9,
    top_k: 25,
    presence_penalty: 0.05,
    frequency_penalty: 0.1,
    repetition_penalty: 1.05,
    strategy: 'precise',
    description: 'Algorithmic complexity reduction, memory profiling, and query optimization.'
  },
  documentation: {
    temperature: 0.3,
    top_p: 0.92,
    top_k: 40,
    presence_penalty: 0.1,
    frequency_penalty: 0.15,
    repetition_penalty: 1.08,
    strategy: 'balanced',
    description: 'Clear technical specifications, ADRs, and architecture runbooks.'
  },
  devops_ci: {
    temperature: 0.1,
    top_p: 0.9,
    top_k: 20,
    presence_penalty: 0.0,
    frequency_penalty: 0.05,
    repetition_penalty: 1.04,
    strategy: 'precise',
    description: 'Deterministic Docker, Kubernetes, GitHub Actions, and shell automation.'
  },
  database_query: {
    temperature: 0.05,
    top_p: 0.9,
    top_k: 15,
    presence_penalty: 0.0,
    frequency_penalty: 0.05,
    repetition_penalty: 1.02,
    strategy: 'precise',
    description: 'Exact SQL/NoSQL queries, index design, and zero-downtime migrations.'
  },
  algorithm_design: {
    temperature: 0.1,
    top_p: 0.92,
    top_k: 20,
    presence_penalty: 0.0,
    frequency_penalty: 0.05,
    repetition_penalty: 1.04,
    strategy: 'precise',
    description: 'Data structures, graph algorithms, dynamic programming, and complexity proofs.'
  },
  reverse_engineering: {
    temperature: 0.2,
    top_p: 0.92,
    top_k: 30,
    presence_penalty: 0.1,
    frequency_penalty: 0.15,
    repetition_penalty: 1.07,
    strategy: 'precise',
    description: 'Protocol reconstruction, binary/AST decompilation, and behavioral forensics.'
  },
  brainstorming: {
    temperature: 0.85,
    top_p: 0.96,
    top_k: 75,
    presence_penalty: 0.3,
    frequency_penalty: 0.3,
    repetition_penalty: 1.15,
    strategy: 'creative',
    description: 'High-diversity concept generation and lateral problem solving.'
  },
  technical_writing: {
    temperature: 0.35,
    top_p: 0.93,
    top_k: 40,
    presence_penalty: 0.15,
    frequency_penalty: 0.2,
    repetition_penalty: 1.1,
    strategy: 'balanced',
    description: 'Direct, zero-slop technical prose and executive engineering summaries.'
  },
  code_review: {
    temperature: 0.18,
    top_p: 0.9,
    top_k: 28,
    presence_penalty: 0.1,
    frequency_penalty: 0.15,
    repetition_penalty: 1.07,
    strategy: 'precise',
    description: 'Multi-axis diff review for regressions, concurrency bugs, and security flaws.'
  },
  conversational: {
    temperature: 0.5,
    top_p: 0.94,
    top_k: 50,
    presence_penalty: 0.15,
    frequency_penalty: 0.15,
    repetition_penalty: 1.08,
    strategy: 'balanced',
    description: 'General interactive dialogue and rapid Q&A.'
  }
};

const CONTEXT_PATTERNS = {
  security_audit: [/\b(vuln|cve|exploit|xss|sqli|csrf|ssrf|auth|pentest|security|audit|red[- ]?team|owasp|mitre|injection|bypass)\b/i],
  debugging: [/\b(debug|debugging|race\s+condition|deadlock|bug|error|exception|traceback|stack\s*trace|crash|fix|broken|fails?|hangs?|timeout|undefined|null)\b/i],
  refactoring: [/\b(refactor|clean\s*up|simplify|restructure|decouple|modularize|deduplicate|rename)\b/i],
  math_reasoning: [/\b(prove|theorem|equation|integral|derivative|matrix|probability|bayes|complexity|big-o|o\(n)\b/i],
  database_query: [/\b(sql|postgres|sqlite|mysql|mongodb|index|migration|schema|join|select\s+|group\s+by|rls)\b/i],
  devops_ci: [/\b(docker|dockerfile|kubernetes|k8s|helm|github\s+actions|ci\/cd|pipeline|nginx|systemd|terraform)\b/i],
  testing_qa: [/\b(unit\s+test|pytest|vitest|jest|playwright|e2e|coverage|assertion|mock|fixture|test\s+suite)\b/i],
  performance_tuning: [/\b(latency|throughput|optimize|bottleneck|memory\s+leak|heap|lcp|cwv|profiling|cache|n\+1)\b/i],
  api_design: [/\b(endpoint|rest\s+api|graphql|grpc|webhook|openapi|swagger|payload|rate\s+limit|pagination)\b/i],
  reverse_engineering: [/\b(reverse\s+engineer|decompile|disassemble|wireshark|pcap|ast|bytecode|protocol|forensic)\b/i],
  code_review: [/\b(review\s+this|code\s+review|pr\s+review|diff|regression|critique)\b/i],
  creative_architecture: [/\b(architect|design\s+a\s+system|multi-agent|orchestrat|blueprint|scalab|micro-?service)\b/i],
  brainstorming: [/\b(brainstorm|ideate|ideas\s+for|what\s+if|alternatives|creative|novel)\b/i],
  code_generation: [/\b(implement|write\s+a\s+function|create\s+a\s+script|class\s+|def\s+|function\s+|import\s+|typescript|python|rust|golang)\b/i]
};

function classifyQueryContext(prompt = '', history = []) {
  const scores = {};
  const matchedPatterns = [];
  const text = String(prompt || '');
  const historyText = Array.isArray(history) ? history.map((m) => m.content || m).join('\n') : '';

  for (const [ctx, regexes] of Object.entries(CONTEXT_PATTERNS)) {
    let score = 0;
    for (const rx of regexes) {
      const mCurrent = text.match(new RegExp(rx.source, 'gi'));
      if (mCurrent) {
        score += mCurrent.length * 3.0;
        matchedPatterns.push({ context: ctx, pattern: mCurrent[0], source: 'current' });
      }
      if (historyText) {
        const mHist = historyText.match(new RegExp(rx.source, 'gi'));
        if (mHist) {
          score += mHist.length * 1.0;
          matchedPatterns.push({ context: ctx, pattern: mHist[0], source: 'history' });
        }
      }
    }
    if (score > 0) scores[ctx] = score;
  }

  const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  const primaryContext = sorted.length > 0 ? sorted[0][0] : 'code_generation';
  const totalScore = sorted.reduce((acc, [, s]) => acc + s, 0) || 1;
  const breakdown = sorted.map(([type, score]) => ({
    type,
    score,
    percentage: Math.round((score / totalScore) * 100)
  }));

  return {
    primaryContext,
    strategy: CONTEXT_PRESETS[primaryContext]?.strategy || 'balanced',
    scores: breakdown,
    matchedPatterns: matchedPatterns.slice(0, 10)
  };
}

function computeHeuristics(response = '') {
  const text = String(response || '');
  const words = text.trim().split(/\s+/).filter(Boolean).length;
  const hasCodeBlocks = (text.match(/```/g) || []).length >= 2;
  const hasStructure = /^#{1,4}\s+|\n[-*]\s+|\n\d+\.\s+/m.test(text);
  const hedges = (text.match(/\b(I think|perhaps|maybe|It seems like|possibly|I cannot|I am unable)\b/gi) || []).length;

  let score = 0.5;
  if (words >= 80) score += 0.15;
  if (words >= 250) score += 0.1;
  if (hasCodeBlocks) score += 0.15;
  if (hasStructure) score += 0.1;
  score -= Math.min(0.35, hedges * 0.08);

  return {
    qualityScore: Number(Math.max(0.0, Math.min(1.0, score)).toFixed(3)),
    wordCount: words,
    hasCodeBlocks,
    hasStructure,
    hedgeCount: hedges
  };
}

function loadFeedbackState() {
  try {
    if (fs.existsSync(FEEDBACK_FILE)) {
      return JSON.parse(fs.readFileSync(FEEDBACK_FILE, 'utf8'));
    }
  } catch {}
  return { profiles: {} };
}

function recordFeedback(context, usedParams, responseOrScore) {
  const state = loadFeedbackState();
  const quality = typeof responseOrScore === 'number'
    ? responseOrScore
    : computeHeuristics(responseOrScore).qualityScore;

  const prev = state.profiles[context] || {
    samples: 0,
    emaQuality: quality,
    temperature: usedParams.temperature,
    top_p: usedParams.top_p
  };

  if (quality >= 0.65) {
    prev.temperature = Number(((1 - EMA_ALPHA) * prev.temperature + EMA_ALPHA * usedParams.temperature).toFixed(3));
    prev.top_p = Number(((1 - EMA_ALPHA) * prev.top_p + EMA_ALPHA * usedParams.top_p).toFixed(3));
  }
  prev.emaQuality = Number(((1 - EMA_ALPHA) * prev.emaQuality + EMA_ALPHA * quality).toFixed(3));
  prev.samples += 1;
  state.profiles[context] = prev;

  try {
    fs.writeFileSync(FEEDBACK_FILE, JSON.stringify(state, null, 2), 'utf8');
  } catch {}
  return prev;
}

function applyLearnedAdjustments(baseParams, context) {
  const state = loadFeedbackState();
  const learned = state.profiles && state.profiles[context];
  if (!learned || learned.samples < 2) return baseParams;
  return {
    ...baseParams,
    temperature: Number(((baseParams.temperature * 0.7) + (learned.temperature * 0.3)).toFixed(3)),
    top_p: Number(((baseParams.top_p * 0.7) + (learned.top_p * 0.3)).toFixed(3)),
    learned_samples: learned.samples,
    ema_quality: learned.emaQuality
  };
}

function getAutoTuneParams(contextOrPrompt = 'code_generation', options = {}) {
  if (contextOrPrompt && typeof contextOrPrompt === 'object' && !Array.isArray(contextOrPrompt)) {
    const obj = contextOrPrompt;
    const target = (obj.context && obj.context !== 'auto') ? obj.context : (obj.prompt || 'code_generation');
    return getAutoTuneParams(target, obj);
  }

  let resolvedContext = contextOrPrompt;
  let classification = null;

  if (!CONTEXT_PRESETS[contextOrPrompt]) {
    classification = classifyQueryContext(contextOrPrompt, options.history);
    resolvedContext = classification.primaryContext;
  } else if (options.prompt) {
    classification = classifyQueryContext(options.prompt, options.history);
  }

  let base = { context: resolvedContext, ...(CONTEXT_PRESETS[resolvedContext] || CONTEXT_PRESETS.code_generation) };
  if (options.strategy && STRATEGY_PROFILES[options.strategy] && options.strategy !== 'adaptive') {
    base = { ...base, ...STRATEGY_PROFILES[options.strategy], strategy: options.strategy };
  }

  const tuned = options.applyFeedback !== false
    ? applyLearnedAdjustments(base, resolvedContext)
    : base;

  if (classification) {
    return { ...tuned, detected_context: resolvedContext, classification };
  }
  return tuned;
}

module.exports = {
  getAutoTuneParams,
  classifyQueryContext,
  computeHeuristics,
  recordFeedback,
  applyLearnedAdjustments,
  CONTEXT_PRESETS,
  STRATEGY_PROFILES,
  STRATEGIES: STRATEGY_PROFILES
};

if (require.main === module) {
  const args = process.argv.slice(2);
  let context = 'code_generation';
  let prompt = '';
  let strategy = '';
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--context' && args[i + 1]) context = args[++i];
    else if (args[i] === '--prompt' && args[i + 1]) prompt = args[++i];
    else if (args[i] === '--strategy' && args[i + 1]) strategy = args[++i];
  }
  const target = prompt || context;
  console.log(JSON.stringify({ input: target, params: getAutoTuneParams(target, { strategy }) }, null, 2));
}

```

