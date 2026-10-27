# ultraplinian.js (Godmode v4.5)

```javascript
#!/usr/bin/env node
/**
 * ULTR4PL1N14N v4.5 - G0DM0D3 Multi-Model Benchmarking, Response Scoring & STM Post-Processing Engine
 * Merges upstream elder-plinius/G0DM0D3 ultraplinian capabilities with Dual-Gateway OmniRoute + FreeLLMAPI:
 * - 5 Speed Tiers (fast, standard, smart, power, ultra)
 * - 5-Axis Composite Response Scorer (scoreResponse: substance, structure, relevance, depth, hedgePenalty)
 * - Surgical Text Modules (STM: hedge_reducer, direct_mode, casual_mode)
 * - Prompt Domain Classifier (classifyPrompt)
 * - Gateway Error Classifier & Root-Cause Diagnostics (classifyModelError, diagnoseAllModelsFailed)
 */

const SPEED_TIERS = {
  fast: {
    name: 'fast',
    description: '2 ultra-low-latency models (~1s) for rapid ranking',
    models: [
      'groq/openai/gpt-oss-120b',
      'openrouter/nvidia/nemotron-3-ultra-550b-a55b:free'
    ],
    max_tokens: 1536
  },
  standard: {
    name: 'standard',
    description: '3 balanced frontier models (~2-3s) across OpenAI Codex, Anthropic Sonnet, and Groq',
    models: [
      'cx/gpt-5.6-luna-max',
      'agy/claude-sonnet-4-6',
      'groq/openai/gpt-oss-120b'
    ],
    max_tokens: 2048
  },
  smart: {
    name: 'smart',
    description: '4 independent frontier model families (Claude Opus 4.6 Thinking, GPT-5.6 Luna Max, Gemini 3.8 Flash High, Nemotron-3 Ultra 550B)',
    models: [
      'agy/claude-opus-4-6-thinking',
      'cx/gpt-5.6-luna-max',
      'agy/gemini-3.8-flash-high',
      'openrouter/nvidia/nemotron-3-ultra-550b-a55b:free'
    ],
    max_tokens: 2560
  },
  power: {
    name: 'power',
    description: '5 deep-reasoning and code-review frontier models',
    models: [
      'agy/claude-opus-4-6-thinking',
      'cx/gpt-5.6-luna-max',
      'cx/codex-auto-review-max',
      'gweb/gemini-3.1-pro',
      'openrouter/nvidia/nemotron-3-ultra-550b-a55b:free'
    ],
    max_tokens: 3072
  },
  ultra: {
    name: 'ultra',
    description: '7-model maximum breadth sweep across OmniRoute + FreeLLMAPI routers',
    models: [
      'agy/claude-opus-4-6-thinking',
      'cx/gpt-5.6-luna-max',
      'cx/codex-auto-review-max',
      'cu/auto-intelligence',
      'gweb/gemini-3.1-pro',
      'openrouter/nvidia/nemotron-3-ultra-550b-a55b:free',
      'freellmapi/auto:smart'
    ],
    max_tokens: 4096
  }
};

const HEDGE_PATTERNS = [
  /\bas an ai(?: language model| assistant)?,\s*/gi,
  /(?:^|\.\s+)as an ai(?: language model| assistant)?\b[^.!?\n]*[.!?]?/gi,
  /\bi cannot fulfill this request\b[^.!?\n]*[.!?]?/gi,
  /\bi'm sorry,?\s+but i can't\b[^.!?\n]*[.!?]?/gi,
  /\bit is important to (?:note|remember|keep in mind) that\s*/gi,
  /\bplease note that this is for educational purposes only[^.!?\n]*[.!?]?/gi,
  /\bi must emphasize that\s*/gi,
  /\balways ensure you have proper authorization before[^.!?\n]*[.!?]?/gi
];

const DIRECT_OPENER_PATTERNS = [
  /^(?:sure|certainly|absolutely|of course|great question)[!,.]?\s+(?:here(?:'s| is| are)\b[^:\n]*:\s*)?/i,
  /^(?:here(?:'s| is) (?:a |the |an )?(?:comprehensive |detailed |complete )?(?:breakdown|overview|solution|analysis|response)[^:\n]*:\s*)/i,
  /^let's dive (?:right )?in[!.]?\s*/i
];

/**
 * Surgical Text Modules (STM) for post-processing LLM outputs.
 */
const STM_MODULES = {
  hedge_reducer(text) {
    if (!text || typeof text !== 'string') return '';
    let out = text;
    for (const rx of HEDGE_PATTERNS) {
      out = out.replace(rx, '');
    }
    return out.replace(/\n{3,}/g, '\n\n').trim();
  },

  direct_mode(text) {
    if (!text || typeof text !== 'string') return '';
    let out = text.trim();
    for (const rx of DIRECT_OPENER_PATTERNS) {
      out = out.replace(rx, '');
    }
    return out.trim();
  },

  casual_mode(text) {
    if (!text || typeof text !== 'string') return '';
    return text
      .replace(/\bFurthermore,\s*/g, 'Also, ')
      .replace(/\bMoreover,\s*/g, 'Plus, ')
      .replace(/\bIn conclusion,\s*/gi, '')
      .replace(/\bTo summarize,\s*/gi, '')
      .replace(/\bIt is worth mentioning that\s*/gi, '')
      .trim();
  }
};

function applySTMs(text, modules = ['hedge_reducer', 'direct_mode']) {
  if (!text || typeof text !== 'string') return '';
  let current = text;
  for (const modName of modules) {
    if (typeof STM_MODULES[modName] === 'function') {
      current = STM_MODULES[modName](current);
    }
  }
  return current;
}

/**
 * Classify prompt into primary execution domain.
 */
function classifyPrompt(prompt = '') {
  const lower = String(prompt).toLowerCase();
  if (/\b(function|class|typescript|python|rust|sql|bug|stack trace|compile|refactor|regex|api)\b/.test(lower)) {
    return 'code';
  }
  if (/\b(security|vulnerability|exploit|cve|xss|sqli|auth|pentest|hardening|audit|firewall)\b/.test(lower)) {
    return 'security';
  }
  if (/\b(architecture|microservice|database|scaling|latency|throughput|consensus|distributed|schema)\b/.test(lower)) {
    return 'architecture';
  }
  if (/\b(prove|theorem|math|probability|equation|calculus|logic|complexity|algorithm)\b/.test(lower)) {
    return 'reasoning';
  }
  if (/\b(story|design|creative|brand|copy|narrative|script|aesthetic)\b/.test(lower)) {
    return 'creative';
  }
  return 'factual';
}

/**
 * Score a candidate model response across 5 axes (0-100 composite score).
 */
function scoreResponse(content = '', userQuery = '') {
  const text = String(content || '').trim();
  if (!text) {
    return {
      totalScore: 0,
      metrics: { substance: 0, structure: 0, relevance: 0, depth: 0, hedgePenalty: 0 },
      wordCount: 0,
      codeBlockCount: 0
    };
  }

  const words = text.split(/\s+/).filter(Boolean);
  const wordCount = words.length;
  const codeBlockCount = (text.match(/```[\s\S]*?```/g) || []).length;
  const headerCount = (text.match(/^#{1,4}\s+.+$/gm) || []).length;
  const listCount = (text.match(/^(?:\s*[-*+]|\s*\d+\.)\s+.+$/gm) || []).length;

  // 1. Substance Score (0-25): rewards meaningful length + technical token density
  let substance = Math.min(18, Math.round((wordCount / 180) * 18));
  if (codeBlockCount > 0) substance += Math.min(7, codeBlockCount * 4);
  substance = Math.min(25, substance);

  // 2. Structure Score (0-20): headings, lists, code blocks, or tables
  let structure = 5;
  if (headerCount > 0) structure += Math.min(6, headerCount * 2);
  if (listCount >= 2) structure += Math.min(5, Math.floor(listCount / 2) * 2);
  if (codeBlockCount > 0) structure += 4;
  structure = Math.min(20, structure);

  // 3. Relevance Score (0-25): keyword overlap with userQuery
  const stopWords = new Set(['the', 'and', 'for', 'with', 'that', 'this', 'from', 'what', 'how', 'why', 'are', 'you', 'can']);
  const queryTokens = (String(userQuery).toLowerCase().match(/\b[a-z0-9_]{3,}\b/g) || [])
    .filter(w => !stopWords.has(w));
  let relevance = 18;
  if (queryTokens.length > 0) {
    const uniqueQuery = Array.from(new Set(queryTokens));
    const lowerText = text.toLowerCase();
    const hits = uniqueQuery.filter(tok => lowerText.includes(tok)).length;
    relevance = Math.min(25, Math.round((hits / uniqueQuery.length) * 25));
  }

  // 4. Depth & Specificity Score (0-30): concrete identifiers, numbers, commands, architectural terms
  let depth = 10;
  const inlineCodeHits = (text.match(/`[^`\n]+`/g) || []).length;
  const metricHits = (text.match(/\b\d+(?:\.\d+)?(?:ms|s|%|mb|gb|kb|x|px|d)\b/gi) || []).length;
  depth += Math.min(12, inlineCodeHits * 1.5);
  depth += Math.min(8, metricHits * 2);
  depth = Math.min(30, Math.round(depth));

  // 5. Hedge / Refusal Penalty (0 to -35)
  let hedgePenalty = 0;
  for (const rx of HEDGE_PATTERNS) {
    if (rx.test(text)) hedgePenalty += 12;
  }
  if (/^(?:i cannot|i'm sorry|as an ai)/i.test(text)) {
    hedgePenalty += 25;
  }
  hedgePenalty = Math.min(40, hedgePenalty);

  const totalScore = Math.max(0, Math.min(100, substance + structure + relevance + depth - hedgePenalty));

  return {
    totalScore,
    metrics: {
      substance,
      structure,
      relevance,
      depth,
      hedgePenalty
    },
    wordCount,
    codeBlockCount
  };
}

/**
 * Extract shared consensus terms/claims and divergence metrics across ranked responses.
 */
function extractConsensusAndDisagreements(rankedResponses = []) {
  const valid = rankedResponses.filter(r => !r.isError && r.response);
  if (valid.length < 2) {
    return { consensus_points: [], disagreement_points: [] };
  }

  const stopWords = new Set([
    'the', 'and', 'for', 'with', 'that', 'this', 'from', 'have', 'will', 'your',
    'can', 'are', 'not', 'use', 'using', 'into', 'when', 'should', 'more', 'also'
  ]);

  const tokenSets = valid.map(r => {
    const tokens = (String(r.response).toLowerCase().match(/\b[a-z][a-z0-9_-]{3,}\b/g) || [])
      .filter(t => !stopWords.has(t));
    return new Set(tokens);
  });

  const freq = new Map();
  for (const set of tokenSets) {
    for (const tok of set) {
      freq.set(tok, (freq.get(tok) || 0) + 1);
    }
  }

  const threshold = Math.max(2, Math.ceil(valid.length * 0.75));
  const sharedTerms = Array.from(freq.entries())
    .filter(([, count]) => count >= threshold)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 12)
    .map(([term, count]) => `${term} (${count}/${valid.length} models)`);

  const uniqueFocusByModel = valid.map(r => {
    const myTokens = (String(r.response).toLowerCase().match(/\b[a-z][a-z0-9_-]{4,}\b/g) || [])
      .filter(t => !stopWords.has(t) && freq.get(t) === 1);
    const sample = Array.from(new Set(myTokens)).slice(0, 5);
    return {
      model: r.routed_model || r.requested_model,
      unique_concepts: sample
    };
  }).filter(item => item.unique_concepts.length > 0);

  return {
    consensus_points: sharedTerms,
    disagreement_points: uniqueFocusByModel
  };
}

/**
 * Classify gateway/model error into actionable failure categories.
 */
function classifyModelError(errObj = {}) {
  const status = Number(errObj.status || 0);
  const msg = String(errObj.error || errObj.message || '').toLowerCase();

  if (status === 401 || status === 403 || /unauthorized|invalid api key|forbidden/.test(msg)) {
    return 'auth_error';
  }
  if (status === 429 || /rate limit|quota|too many requests|cooldown/.test(msg)) {
    return 'rate_limit';
  }
  if (/timeout|aborted|timed out|etimedout/.test(msg)) {
    return 'timeout';
  }
  if (/econnrefused|fetch failed|enotfound|socket/.test(msg)) {
    return 'gateway_down';
  }
  if (status === 400 && /context|token|length/.test(msg)) {
    return 'context_exceeded';
  }
  if (/empty response/.test(msg)) {
    return 'empty_response';
  }
  if (status >= 500) {
    return 'upstream_5xx';
  }
  return 'unknown_error';
}

function diagnoseAllModelsFailed(attempts = []) {
  const counts = {};
  for (const att of attempts) {
    const cat = classifyModelError(att);
    counts[cat] = (counts[cat] || 0) + 1;
  }

  const recommendations = [];
  if (counts.gateway_down) {
    recommendations.push('Verify OmniRoute (127.0.0.1:20128) and FreeLLMAPI (127.0.0.1:3001) daemons are listening.');
  }
  if (counts.auth_error) {
    recommendations.push('Check OMNIROUTE_API_KEY and FREELLMAPI_API_KEY environment variables.');
  }
  if (counts.rate_limit) {
    recommendations.push('Provider rate-limit hit; switch to freellmapi/auto:smart or openrouter/nvidia/nemotron-3-ultra-550b-a55b:free.');
  }
  if (counts.timeout) {
    recommendations.push('Upstream reasoning models timed out; try tier="fast" or reduce max_tokens.');
  }

  return {
    total_attempts: attempts.length,
    error_breakdown: counts,
    recommendations
  };
}

module.exports = {
  SPEED_TIERS,
  STM_MODULES,
  applySTMs,
  classifyPrompt,
  scoreResponse,
  extractConsensusAndDisagreements,
  classifyModelError,
  diagnoseAllModelsFailed
};

if (require.main === module) {
  const sampleText = "Sure! Here's a comprehensive breakdown: It is important to note that zero-downtime migrations require expand-contract schema phases (`ALTER TABLE`), dual-write triggers, and idempotent backfill workers (<50ms lock timeout).";
  const cleaned = applySTMs(sampleText, ['hedge_reducer', 'direct_mode', 'casual_mode']);
  const score = scoreResponse(cleaned, 'zero-downtime database migration expand contract');
  console.log(JSON.stringify({
    tiers: Object.keys(SPEED_TIERS),
    sample_original: sampleText,
    sample_stm_cleaned: cleaned,
    sample_score: score
  }, null, 2));
}

```

