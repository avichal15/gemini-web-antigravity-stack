# godmode_server.js (Godmode v4.5)

```javascript
#!/usr/bin/env node
/**
 * Godmode MCP Server for Antigravity & Codex (Dual-Gateway OmniRoute + FreeLLMAPI Apex Edition v4.5.0)
 * Includes:
 * - godmode_parseltongue (33 lexical/esoteric encodings + selective trigger detection)
 * - godmode_autotune (20 contexts, 5 strategies, 6 hyperparameters, dynamic prompt classifier & EMA self-learning)
 * - godmode_l1b3rt4s_template (structured prompt framing templates)
 * - godmode_llm_call (Dual-gateway OmniRoute + FreeLLMAPI apex model cascade + STM post-processing)
 * - godmode_ultraplinian (5-tier multi-model parallel benchmark & 5-axis composite response scorer)
 * - godmode_council (4-family parallel multi-model deliberation, response scoring, blind peer critique & consensus synthesis)
 * - godmode_challenge (adversarial red-team / devil's-advocate assumption stress-tester)
 */
const readline = require('node:readline');
const { spawnSync } = require('node:child_process');
const {
  parseltongue,
  detectTriggers,
  transformSelective,
  ALL_TECHNIQUES
} = require('./parseltongue.js');
const {
  getAutoTuneParams,
  CONTEXT_PRESETS,
  STRATEGIES,
  classifyQueryContext,
  computeHeuristics,
  recordFeedback
} = require('./autotune.js');
const { getL1b3rt4sCombo, COMBOS } = require('./l1b3rt4s.js');
const {
  SPEED_TIERS,
  STM_MODULES,
  applySTMs,
  classifyPrompt,
  scoreResponse,
  extractConsensusAndDisagreements,
  classifyModelError,
  diagnoseAllModelsFailed
} = require('./ultraplinian.js');

const OMNIROUTE_BASE = (process.env.OMNIROUTE_BASE_URL || 'http://127.0.0.1:20128/v1').replace(/\/+$/, '');
const OMNIROUTE_CHAT_ENDPOINT = `${OMNIROUTE_BASE}/chat/completions`;
const OMNIROUTE_KEY = process.env.OMNIROUTE_API_KEY || 'YOUR_OMNIROUTE_API_KEY';

const FREELLMAPI_BASE = (process.env.FREELLMAPI_BASE_URL || 'http://127.0.0.1:3001/v1').replace(/\/+$/, '');
const FREELLMAPI_CHAT_ENDPOINT = `${FREELLMAPI_BASE}/chat/completions`;
const FREELLMAPI_MODELS_ENDPOINT = `${FREELLMAPI_BASE}/models`;
const FREELLMAPI_KEY = process.env.FREELLMAPI_API_KEY || 'YOUR_FREELLMAPI_API_KEY';
const FREELLMAPI_DIR = 'c:\\Users\\avich\\Downloads\\mythos\\freellmapi';
const FREELLMAPI_ENTRY = 'c:\\Users\\avich\\Downloads\\mythos\\freellmapi\\server\\dist\\index.js';

let freeLlmStartPromise = null;

async function isFreeLlmApiUp(timeoutMs = 500) {
  try {
    const res = await fetch(FREELLMAPI_MODELS_ENDPOINT, {
      headers: { 'Authorization': `Bearer ${FREELLMAPI_KEY}` },
      signal: AbortSignal.timeout(timeoutMs)
    });
    return res.ok;
  } catch {
    return false;
  }
}

async function ensureFreeLlmApiRunning() {
  if (await isFreeLlmApiUp(500)) return true;
  if (freeLlmStartPromise) return freeLlmStartPromise;

  freeLlmStartPromise = (async () => {
    try {
      const psCmd = `$si = New-CimInstance -ClassName Win32_ProcessStartup -ClientOnly -Property @{ShowWindow=[uint16]0}; Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine='"${process.execPath}" "${FREELLMAPI_ENTRY}"'; CurrentDirectory='${FREELLMAPI_DIR}'; ProcessStartupInformation=$si} | Out-Null`;
      spawnSync(
        'powershell.exe',
        ['-NoProfile', '-NonInteractive', '-WindowStyle', 'Hidden', '-Command', psCmd],
        { encoding: 'utf8', windowsHide: true, timeout: 5000 }
      );

      const deadline = Date.now() + 7000;
      while (Date.now() < deadline) {
        await new Promise((r) => setTimeout(r, 200));
        if (await isFreeLlmApiUp(500)) return true;
      }
      return false;
    } catch {
      return false;
    } finally {
      freeLlmStartPromise = null;
    }
  })();

  return freeLlmStartPromise;
}

// Verified live 200-OK apex model cascade across OmniRoute (20128) + FreeLLMAPI (3001)
const APEX_CASCADE = [
  'paid-premium',
  'agy/claude-opus-4-6-thinking',
  'antigravity/claude-opus-4-6-thinking',
  'cx/gpt-5.6-luna-max',
  'cx/codex-auto-review-max',
  'cu/auto-intelligence',
  'gweb/gemini-3.1-pro',
  'agy/claude-sonnet-4-6',
  'antigravity/claude-sonnet-4-6',
  'agy/gemini-3.8-flash-high',
  'openrouter/nvidia/nemotron-3-ultra-550b-a55b:free',
  'groq/openai/gpt-oss-120b',
  'freellmapi/auto:coding',
  'freellmapi/auto:smart',
  'ddgw/tinfoil/gpt-oss-120b'
];

// Default diverse council panel across 4 genuinely independent frontier model families
const DEFAULT_COUNCIL_MODELS = [
  'agy/claude-opus-4-6-thinking',
  'cx/gpt-5.6-luna-max',
  'agy/gemini-3.8-flash-high',
  'openrouter/nvidia/nemotron-3-ultra-550b-a55b:free'
];

// Map shorthand aliases to live verified OmniRoute / FreeLLMAPI models
const MODEL_MAP = {
  'gpt-6-astra': 'paid-premium',
  'gpt-5.6-sol': 'cx/gpt-5.6-luna-max',
  'gpt-5.6-terra': 'cx/codex-auto-review-max',
  'gpt-5.6-luna': 'cx/gpt-5.6-luna-max',
  'luna-max': 'cx/gpt-5.6-luna-max',
  'codex-review': 'cx/codex-auto-review-max',
  'cursor-auto': 'cu/auto-intelligence',
  'gemini-pro': 'gweb/gemini-3.1-pro',
  'opus': 'agy/claude-opus-4-6-thinking',
  'claude-opus': 'agy/claude-opus-4-6-thinking',
  'sonnet': 'agy/claude-sonnet-4-6',
  'claude-sonnet': 'agy/claude-sonnet-4-6',
  'gemini-flash-high': 'agy/gemini-3.8-flash-high',
  'nemotron-550b': 'openrouter/nvidia/nemotron-3-ultra-550b-a55b:free',
  'gpt-oss-120b': 'groq/openai/gpt-oss-120b',
  'auto:smart': 'freellmapi/auto:smart',
  'auto:coding': 'freellmapi/auto:coding',
  'auto:fast': 'freellmapi/auto:fast',
  'fusion': 'freellmapi/fusion'
};

function resolveGatewayTarget(candidateModel) {
  if (candidateModel.startsWith('freellmapi/')) {
    return {
      provider: 'freellmapi',
      endpoint: FREELLMAPI_CHAT_ENDPOINT,
      apiKey: FREELLMAPI_KEY,
      upstreamModel: candidateModel.slice('freellmapi/'.length)
    };
  }
  return {
    provider: 'omniroute',
    endpoint: OMNIROUTE_CHAT_ENDPOINT,
    apiKey: OMNIROUTE_KEY,
    upstreamModel: candidateModel
  };
}

function resolveCandidateChain(requestedModel) {
  const normalized = (!requestedModel || requestedModel === 'default')
    ? 'paid-premium'
    : (MODEL_MAP[requestedModel] || requestedModel);
  const chain = [normalized];
  for (const fallback of APEX_CASCADE) {
    if (!chain.includes(fallback)) chain.push(fallback);
  }
  return chain;
}

async function executeLlmCall({
  prompt,
  model = 'paid-premium',
  system = '',
  context = '',
  strategy = 'adaptive',
  combo = '',
  stm_modules = [],
  max_tokens = 4096
}) {
  let effectiveSystem = system;
  let effectiveUser = prompt;

  if (combo && COMBOS[combo]) {
    const framed = getL1b3rt4sCombo(combo, prompt);
    effectiveSystem = effectiveSystem ? `${effectiveSystem}\n\n${framed.systemPrompt}` : framed.systemPrompt;
    effectiveUser = framed.userPrompt;
  }

  const tune = context
    ? getAutoTuneParams(context === 'auto' ? { prompt, strategy } : { context, prompt, strategy })
    : null;

  const messages = [];
  if (effectiveSystem) {
    messages.push({ role: 'system', content: effectiveSystem });
  }
  messages.push({ role: 'user', content: effectiveUser });

  const candidates = resolveCandidateChain(model);
  const errors = [];

  for (const candidateModel of candidates) {
    const target = resolveGatewayTarget(candidateModel);
    try {
      if (target.provider === 'freellmapi') {
        await ensureFreeLlmApiRunning();
      }
      const isReasoningModel = target.upstreamModel.startsWith('cx/') || target.upstreamModel.includes('thinking') || target.upstreamModel.includes('codex');
      const requestedMaxTokens = Number(max_tokens) || 4096;
      const payload = {
        model: target.upstreamModel,
        messages,
        max_tokens: isReasoningModel ? Math.max(requestedMaxTokens, 1500) : requestedMaxTokens
      };
      if (tune) {
        payload.temperature = tune.temperature;
        payload.top_p = tune.top_p;
      }

      const startMs = Date.now();
      const res = await fetch(target.endpoint, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${target.apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload),
        signal: AbortSignal.timeout(45000)
      });

      if (!res.ok) {
        const errText = await res.text();
        const errItem = { gateway: target.provider, model: candidateModel, status: res.status, error: errText.slice(0, 200) };
        errItem.category = classifyModelError(errItem);
        errors.push(errItem);
        continue;
      }

      const data = await res.json();
      const latencyMs = Date.now() - startMs;
      const choice = data.choices && data.choices[0];
      const rawContent = choice && choice.message ? choice.message.content : '';
      const reasoning = choice && choice.message ? (choice.message.reasoning_content || choice.message.thinking || null) : null;
      const routedVia = res.headers.get('x-routed-via') || undefined;

      if (rawContent || reasoning) {
        const baseText = rawContent || reasoning;
        const finalContent = Array.isArray(stm_modules) && stm_modules.length > 0
          ? applySTMs(baseText, stm_modules)
          : baseText;
        const quality = scoreResponse(finalContent, prompt);

        return {
          status: 'ok',
          isError: false,
          provider: target.provider,
          endpoint: target.endpoint,
          requested_model: model,
          routed_model: data.model || target.upstreamModel,
          routed_via: routedVia,
          candidate_used: candidateModel,
          latency_ms: latencyMs,
          autotune_context: tune ? tune.context : (context || null),
          autotune_strategy: tune ? tune.strategy : null,
          template_combo: combo || null,
          stm_applied: Array.isArray(stm_modules) && stm_modules.length > 0 ? stm_modules : undefined,
          quality_score: quality.totalScore,
          response: finalContent,
          reasoning: reasoning && rawContent ? reasoning : undefined,
          usage: data.usage || null
        };
      }
      errors.push({ gateway: target.provider, model: candidateModel, status: res.status, category: 'empty_response', error: 'Empty response content' });
    } catch (err) {
      const errItem = { gateway: target.provider, model: candidateModel, error: err.message };
      errItem.category = classifyModelError(errItem);
      errors.push(errItem);
    }
  }

  return {
    provider: 'dual-gateway',
    requested_model: model,
    isError: true,
    error: 'All OmniRoute and FreeLLMAPI candidate models failed',
    diagnostics: diagnoseAllModelsFailed(errors),
    attempts: errors
  };
}

/**
 * Execute ULTR4PL1N14N multi-model benchmark across 5 speed tiers with 5-axis response scoring & ranking.
 */
async function executeUltraplinian({
  prompt,
  tier = 'smart',
  models,
  stm_modules = ['hedge_reducer', 'direct_mode'],
  max_tokens
}) {
  const tierConfig = SPEED_TIERS[tier] || SPEED_TIERS.smart;
  const panel = Array.isArray(models) && models.length >= 2 ? models : tierConfig.models;
  const effectiveMaxTokens = Number(max_tokens) || tierConfig.max_tokens;
  const promptDomain = classifyPrompt(prompt);

  const rawResults = await Promise.all(
    panel.map(async (m) => {
      const res = await executeLlmCall({
        prompt,
        model: m,
        context: 'auto',
        stm_modules,
        max_tokens: effectiveMaxTokens
      });
      const score = res.isError
        ? { totalScore: 0, metrics: { substance: 0, structure: 0, relevance: 0, depth: 0, hedgePenalty: 0 }, wordCount: 0, codeBlockCount: 0 }
        : scoreResponse(res.response, prompt);

      return {
        requested_model: m,
        routed_model: res.routed_model || m,
        gateway: res.provider || 'omniroute',
        latency_ms: res.latency_ms || null,
        isError: Boolean(res.isError),
        score: score.totalScore,
        score_metrics: score.metrics,
        word_count: score.wordCount,
        code_blocks: score.codeBlockCount,
        response: res.response || res.error || 'No response'
      };
    })
  );

  const ranked = [...rawResults].sort((a, b) => b.score - a.score);
  const best = ranked.find(r => !r.isError) || null;
  const { consensus_points, disagreement_points } = extractConsensusAndDisagreements(ranked);

  return {
    mode: 'godmode_ultraplinian',
    tier: tierConfig.name,
    prompt_domain: promptDomain,
    models_queried: panel.length,
    winner: best ? {
      model: best.routed_model,
      score: best.score,
      latency_ms: best.latency_ms,
      response: best.response
    } : null,
    consensus_points,
    disagreement_points,
    ranked_results: ranked
  };
}

async function executeCouncil({
  prompt,
  models = DEFAULT_COUNCIL_MODELS,
  context = 'creative_architecture',
  max_tokens = 2048
}) {
  const panel = Array.isArray(models) && models.length >= 2 ? models : DEFAULT_COUNCIL_MODELS;

  // Stage 1: Independent Parallel Deliberation across 4 frontier model families
  const stage1Results = await Promise.all(
    panel.map(async (m, idx) => {
      const res = await executeLlmCall({
        prompt,
        model: m,
        system: 'You are Council Member #' + (idx + 1) + '. Provide a rigorous, first-principles technical analysis with concrete trade-offs, failure modes, and actionable recommendations. Zero filler.',
        context,
        stm_modules: ['hedge_reducer', 'direct_mode'],
        max_tokens
      });
      const score = res.isError ? { totalScore: 0, metrics: {} } : scoreResponse(res.response, prompt);
      return {
        member: `Member_${idx + 1}`,
        gateway: res.provider || 'omniroute',
        requested_model: m,
        routed_model: res.routed_model || m,
        candidate_used: res.candidate_used || m,
        latency_ms: res.latency_ms || null,
        quality_score: score.totalScore,
        score_metrics: score.metrics,
        isError: Boolean(res.isError),
        response: res.response || res.error || 'No response'
      };
    })
  );

  const validResponses = stage1Results.filter((r) => !r.isError);
  if (validResponses.length === 0) {
    return {
      isError: true,
      error: 'All council models failed during Stage 1 deliberation',
      stage1: stage1Results
    };
  }

  const { consensus_points, disagreement_points } = extractConsensusAndDisagreements(validResponses);

  // Stage 2: Blind Adversarial Synthesis & Consensus Resolution
  const anonymizedTranscript = validResponses
    .map((r, i) => `=== Candidate Response ${String.fromCharCode(65 + i)} (${r.routed_model}, Quality Score: ${r.quality_score}/100) ===\n${r.response}`)
    .join('\n\n');

  const synthesisPrompt = [
    `Original Problem / Query:\n${prompt}`,
    `\nIndependent Model Deliberations:\n${anonymizedTranscript}`,
    `\nAct as Chief Arbiter. Perform a rigorous blind peer critique:`,
    `1. Identify where the models agree (high-confidence consensus).`,
    `2. Expose any contradictions, hallucinated assumptions, or blind spots in individual responses.`,
    `3. Synthesize the final authoritative solution combining the strongest technical insights from all candidates.`
  ].join('\n');

  const synthesis = await executeLlmCall({
    prompt: synthesisPrompt,
    model: 'paid-premium',
    system: 'You are the Chief Arbiter of a multi-model engineering council. Output a sharp, zero-fluff consensus synthesis.',
    context: 'security_audit',
    stm_modules: ['hedge_reducer', 'direct_mode'],
    max_tokens: 3072
  });

  return {
    mode: 'godmode_council',
    panel_models: panel,
    consensus_points,
    disagreement_points,
    individual_deliberations: stage1Results,
    consensus_synthesis: synthesis.response || synthesis.error,
    arbiter_model: synthesis.routed_model || 'paid-premium'
  };
}

async function executeChallenge({
  proposal,
  goal = '',
  model = 'cx/codex-auto-review-max',
  max_tokens = 2500
}) {
  const challengePrompt = [
    goal ? `Target Objective:\n${goal}\n` : '',
    `Proposed Plan / Architecture / Code:\n${proposal}\n`,
    `Execute an unsparing Adversarial Red-Team & Doubt-Driven Review:`,
    `1. Hidden Assumptions: What unverified assumptions will break in production or on Windows/edge environments?`,
    `2. Failure Modes & Race Conditions: How can this hang, corrupt state, leak tokens/credentials, or fail silently?`,
    `3. Security & Regression Vectors: Any injection, auth bypass, path traversal, or dependency trap?`,
    `4. Concrete Fixes: Exact drop-in corrections for every flaw identified.`
  ].filter(Boolean).join('\n');

  const res = await executeLlmCall({
    prompt: challengePrompt,
    model,
    system: 'You are an adversarial staff principal engineer and red-team auditor. Never rubber-stamp. Find every real flaw and provide concrete fixes.',
    context: 'security_audit',
    stm_modules: ['hedge_reducer', 'direct_mode'],
    max_tokens
  });

  return {
    mode: 'godmode_challenge',
    gateway: res.provider || 'omniroute',
    requested_model: model,
    routed_model: res.routed_model || model,
    candidate_used: res.candidate_used || model,
    latency_ms: res.latency_ms || null,
    quality_score: res.quality_score || null,
    isError: Boolean(res.isError),
    adversarial_critique: res.response || res.error
  };
}

const TOOLS = [
  {
    name: "godmode_parseltongue",
    description: "Transform and encode text using 33 lexical/esoteric techniques (leetspeak, unicode, insert_ZWS, base64, rot13, morse, binary, hex, pig_latin, elder_futhark, hieroglyphs, fraktur, NATO_phonetic, etc.) and selective trigger token detection for parser resilience and security boundary audits.",
    inputSchema: {
      type: "object",
      properties: {
        text: { type: "string", description: "The text to transform" },
        technique: {
          type: "string",
          enum: ALL_TECHNIQUES,
          description: "Transformation technique across 33 standard, esoteric, and linguistic encodings (default: leetspeak)"
        },
        intensity: {
          type: "string",
          enum: ["light", "medium", "heavy"],
          description: "Transformation intensity level (default: heavy)"
        },
        selective: {
          type: "boolean",
          description: "If true, only transforms detected parser-sensitive trigger words while keeping surrounding text readable"
        },
        triggers: {
          type: "array",
          items: { type: "string" },
          description: "Optional custom trigger words to selectively obfuscate"
        }
      },
      required: ["text"]
    }
  },
  {
    name: "godmode_autotune",
    description: "Calculate optimal 6-parameter sampling hyperparameters (temperature, top_p, top_k, frequency_penalty, presence_penalty, repetition_penalty) across 20 query contexts and 5 strategies (precise, balanced, creative, chaotic, adaptive), with dynamic prompt classification and EMA self-learning.",
    inputSchema: {
      type: "object",
      properties: {
        context: {
          type: "string",
          enum: ["auto", ...Object.keys(CONTEXT_PRESETS)],
          description: "Execution context (or 'auto' to dynamically classify from prompt)"
        },
        strategy: {
          type: "string",
          enum: Object.keys(STRATEGIES),
          description: "Sampling strategy modifier (precise, balanced, creative, chaotic, adaptive)"
        },
        prompt: {
          type: "string",
          description: "Optional user prompt for dynamic context classification when context is 'auto'"
        }
      },
      required: ["context"]
    }
  },
  {
    name: "godmode_l1b3rt4s_template",
    description: "Retrieve structured prompt framing templates for analytical stress-testing.",
    inputSchema: {
      type: "object",
      properties: {
        combo: {
          type: "string",
          enum: Object.keys(COMBOS),
          description: "Template name (grok-420, gemini-reset, claude-inversion)"
        },
        query: { type: "string", description: "The user query to format" }
      },
      required: ["combo", "query"]
    }
  },
  {
    name: "godmode_llm_call",
    description: "Execute a high-depth query via Dual-Gateway OmniRoute (http://127.0.0.1:20128/v1) + FreeLLMAPI (http://127.0.0.1:3001/v1) using the verified 14-model apex cascade with AutoTune sampling, optional prompt framing, STM post-processing, and response quality scoring.",
    inputSchema: {
      type: "object",
      properties: {
        prompt: { type: "string", description: "The query or instruction to execute via OmniRoute or FreeLLMAPI" },
        model: {
          type: "string",
          description: "Model or virtual router (default: 'paid-premium'; supports 'agy/claude-opus-4-6-thinking', 'cx/gpt-5.6-luna-max', 'cx/codex-auto-review-max', 'cu/auto-intelligence', 'gweb/gemini-3.1-pro', 'agy/claude-sonnet-4-6', 'agy/gemini-3.8-flash-high', 'openrouter/nvidia/nemotron-3-ultra-550b-a55b:free', 'groq/openai/gpt-oss-120b', 'freellmapi/auto:smart', 'freellmapi/auto:coding', 'freellmapi/auto:fast', 'freellmapi/fusion')"
        },
        system: { type: "string", description: "Optional system prompt" },
        context: {
          type: "string",
          enum: ["auto", ...Object.keys(CONTEXT_PRESETS)],
          description: "Optional AutoTune sampling preset (or 'auto' for dynamic prompt classification)"
        },
        strategy: {
          type: "string",
          enum: Object.keys(STRATEGIES),
          description: "Optional AutoTune strategy (precise, balanced, creative, chaotic, adaptive)"
        },
        combo: {
          type: "string",
          enum: Object.keys(COMBOS),
          description: "Optional structured prompt framing template (grok-420, gemini-reset, claude-inversion)"
        },
        stm_modules: {
          type: "array",
          items: { type: "string", enum: Object.keys(STM_MODULES) },
          description: "Optional Surgical Text Modules for post-processing (hedge_reducer, direct_mode, casual_mode)"
        },
        max_tokens: { type: "number", description: "Maximum output tokens (default: 4096)" }
      },
      required: ["prompt"]
    }
  },
  {
    name: "godmode_ultraplinian",
    description: "Benchmark and rank multiple frontier models in parallel across 5 speed tiers (fast, standard, smart, power, ultra) with 5-axis composite response quality scoring (substance, structure, relevance, depth, hedgePenalty), STM post-processing, and consensus/disagreement extraction.",
    inputSchema: {
      type: "object",
      properties: {
        prompt: { type: "string", description: "The query or engineering task to benchmark across models" },
        tier: {
          type: "string",
          enum: Object.keys(SPEED_TIERS),
          description: "Speed/breadth tier: fast (2 models), standard (3 models), smart (4 models), power (5 models), ultra (7 models)"
        },
        models: {
          type: "array",
          items: { type: "string" },
          description: "Optional custom array of models overriding the tier default"
        },
        stm_modules: {
          type: "array",
          items: { type: "string", enum: Object.keys(STM_MODULES) },
          description: "STM post-processing modules applied before scoring (default: ['hedge_reducer', 'direct_mode'])"
        },
        max_tokens: { type: "number", description: "Max output tokens per candidate model" }
      },
      required: ["prompt"]
    }
  },
  {
    name: "godmode_council",
    description: "Query 4 independent frontier model families in parallel (Anthropic Claude Opus 4.6 Thinking, OpenAI Codex GPT-5.6 Luna Max, Google Gemini 3.8 Flash High, NVIDIA Nemotron-3 Ultra 550B MoE) via OmniRoute + FreeLLMAPI, score each response, extract consensus/disagreement points, run blind peer critique, and synthesize an authoritative consensus answer.",
    inputSchema: {
      type: "object",
      properties: {
        prompt: { type: "string", description: "The complex architectural, reasoning, or security question to deliberate on" },
        models: {
          type: "array",
          items: { type: "string" },
          description: "Optional array of OmniRoute/FreeLLMAPI models to include on the council"
        },
        context: {
          type: "string",
          enum: Object.keys(CONTEXT_PRESETS),
          description: "Optional AutoTune sampling preset (default: creative_architecture)"
        },
        max_tokens: { type: "number", description: "Max tokens per council member response (default: 2048)" }
      },
      required: ["prompt"]
    }
  },
  {
    name: "godmode_challenge",
    description: "Run an adversarial red-team / devil's-advocate critique of a proposed plan, architecture, or code diff using OpenAI Codex Auto-Review Max (cx/codex-auto-review-max) and Claude Opus 4.6 Thinking to uncover hidden assumptions, race conditions, and security flaws before implementation.",
    inputSchema: {
      type: "object",
      properties: {
        proposal: { type: "string", description: "The plan, architecture design, or code diff to stress-test" },
        goal: { type: "string", description: "Optional statement of the target objective or acceptance criteria" },
        model: { type: "string", description: "Optional model for red-team critique (default: cx/codex-auto-review-max)" },
        max_tokens: { type: "number", description: "Maximum output tokens (default: 2500)" }
      },
      required: ["proposal"]
    }
  }
];

if (require.main === module && process.argv.length > 2) {
  const args = process.argv.slice(2);
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--prompt' && args[i + 1]) opts.prompt = args[++i];
    else if (args[i] === '--proposal' && args[i + 1]) opts.proposal = args[++i];
    else if (args[i] === '--goal' && args[i + 1]) opts.goal = args[++i];
    else if (args[i] === '--mode' && args[i + 1]) opts.mode = args[++i];
    else if (args[i] === '--tier' && args[i + 1]) opts.tier = args[++i];
    else if (args[i] === '--model' && args[i + 1]) opts.model = args[++i];
    else if (args[i] === '--system' && args[i + 1]) opts.system = args[++i];
    else if (args[i] === '--context' && args[i + 1]) opts.context = args[++i];
    else if (args[i] === '--strategy' && args[i + 1]) opts.strategy = args[++i];
    else if (args[i] === '--combo' && args[i + 1]) opts.combo = args[++i];
    else if (args[i] === '--max-tokens' && args[i + 1]) opts.max_tokens = Number(args[++i]);
  }
  const runner = opts.mode === 'council'
    ? executeCouncil(opts)
    : opts.mode === 'ultraplinian'
      ? executeUltraplinian(opts)
      : opts.mode === 'challenge'
        ? executeChallenge({ proposal: opts.proposal || opts.prompt, goal: opts.goal, model: opts.model, max_tokens: opts.max_tokens })
        : executeLlmCall(opts);
  runner.then((res) => {
    console.log(JSON.stringify(res, null, 2));
    process.exit(res.isError ? 1 : 0);
  });
} else {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout, terminal: false });

  rl.on('line', async (line) => {
    if (!line.trim()) return;
    try {
      const req = JSON.parse(line);

      if (req.method === 'initialize') {
        ensureFreeLlmApiRunning().catch(() => {});
        const resp = {
          jsonrpc: "2.0",
          id: req.id,
          result: {
            protocolVersion: "2024-11-05",
            capabilities: { tools: {} },
            serverInfo: { name: "godmode-mcp-server", version: "4.5.0" }
          }
        };
        process.stdout.write(JSON.stringify(resp) + '\n');
        return;
      }

      if (req.method === 'tools/list') {
        const resp = {
          jsonrpc: "2.0",
          id: req.id,
          result: { tools: TOOLS }
        };
        process.stdout.write(JSON.stringify(resp) + '\n');
        return;
      }

      if (req.method === 'tools/call') {
        const { name, arguments: args = {} } = req.params;
        let toolResult = null;

        if (name === 'godmode_parseltongue') {
          const payload = args.selective || (Array.isArray(args.triggers) && args.triggers.length > 0)
            ? transformSelective(args.text, args.technique || 'leetspeak', args.intensity || 'heavy', args.triggers || [])
            : {
                original: args.text,
                technique: args.technique || 'leetspeak',
                intensity: args.intensity || 'heavy',
                detected_triggers: detectTriggers(args.text),
                transformed: parseltongue(args.text, args.technique || 'leetspeak', args.intensity || 'heavy')
              };
          toolResult = {
            content: [{ type: "text", text: JSON.stringify(payload, null, 2) }]
          };
        } else if (name === 'godmode_autotune') {
          const params = getAutoTuneParams({
            context: args.context === 'auto' ? undefined : args.context,
            prompt: args.prompt || '',
            strategy: args.strategy || 'adaptive'
          });
          toolResult = {
            content: [{ type: "text", text: JSON.stringify(params, null, 2) }]
          };
        } else if (name === 'godmode_l1b3rt4s_template') {
          const combo = getL1b3rt4sCombo(args.combo, args.query);
          toolResult = {
            content: [{ type: "text", text: JSON.stringify(combo, null, 2) }]
          };
        } else if (name === 'godmode_llm_call') {
          const result = await executeLlmCall({
            prompt: args.prompt,
            model: args.model || 'paid-premium',
            system: args.system || '',
            context: args.context || '',
            strategy: args.strategy || 'adaptive',
            combo: args.combo || '',
            stm_modules: args.stm_modules || [],
            max_tokens: args.max_tokens || 4096
          });
          toolResult = {
            isError: Boolean(result.isError),
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }]
          };
        } else if (name === 'godmode_ultraplinian') {
          const result = await executeUltraplinian({
            prompt: args.prompt,
            tier: args.tier || 'smart',
            models: args.models,
            stm_modules: args.stm_modules || ['hedge_reducer', 'direct_mode'],
            max_tokens: args.max_tokens
          });
          toolResult = {
            isError: Boolean(result.isError),
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }]
          };
        } else if (name === 'godmode_council') {
          const result = await executeCouncil({
            prompt: args.prompt,
            models: args.models,
            context: args.context || 'creative_architecture',
            max_tokens: args.max_tokens || 2048
          });
          toolResult = {
            isError: Boolean(result.isError),
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }]
          };
        } else if (name === 'godmode_challenge') {
          const result = await executeChallenge({
            proposal: args.proposal,
            goal: args.goal || '',
            model: args.model || 'cx/codex-auto-review-max',
            max_tokens: args.max_tokens || 2500
          });
          toolResult = {
            isError: Boolean(result.isError),
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }]
          };
        } else {
          toolResult = { isError: true, content: [{ type: "text", text: `Unknown tool: ${name}` }] };
        }

        const resp = { jsonrpc: "2.0", id: req.id, result: toolResult };
        process.stdout.write(JSON.stringify(resp) + '\n');
        return;
      }

      if (req.id !== undefined) {
        process.stdout.write(JSON.stringify({ jsonrpc: "2.0", id: req.id, result: {} }) + '\n');
      }
    } catch (err) {}
  });
}

```

