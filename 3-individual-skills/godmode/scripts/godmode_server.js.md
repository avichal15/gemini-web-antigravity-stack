# Reference Asset: `scripts/godmode_server.js`

Converted to Markdown for Gemini Web upload compatibility.

````js
#!/usr/bin/env node
/**
 * Godmode MCP Server for Antigravity & Codex (Dual-Gateway OmniRoute + FreeLLMAPI Apex Edition v4.0.0)
 * Includes:
 * - godmode_parseltongue (lexical encoding & parser boundary audits)
 * - godmode_autotune (context-adaptive sampling parameters)
 * - godmode_l1b3rt4s_template (structured prompt framing templates)
 * - godmode_llm_call (Dual-gateway OmniRoute + FreeLLMAPI apex model cascade execution)
 * - godmode_council (4-family parallel multi-model deliberation, peer critique & consensus synthesis)
 * - godmode_challenge (adversarial red-team / devil's-advocate assumption stress-tester)
 */
const readline = require('node:readline');
const { spawnSync } = require('node:child_process');
const { parseltongue } = require('./parseltongue.js');
const { getAutoTuneParams, CONTEXT_PRESETS } = require('./autotune.js');
const { getL1b3rt4sCombo, COMBOS } = require('./l1b3rt4s.js');

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
  combo = '',
  max_tokens = 4096
}) {
  let effectiveSystem = system;
  let effectiveUser = prompt;

  if (combo && COMBOS[combo]) {
    const framed = getL1b3rt4sCombo(combo, prompt);
    effectiveSystem = effectiveSystem ? `${effectiveSystem}\n\n${framed.systemPrompt}` : framed.systemPrompt;
    effectiveUser = framed.userPrompt;
  }

  const tune = context ? getAutoTuneParams(context) : null;
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
        errors.push({ gateway: target.provider, model: candidateModel, status: res.status, error: errText.slice(0, 200) });
        continue;
      }

      const data = await res.json();
      const choice = data.choices && data.choices[0];
      const content = choice && choice.message ? choice.message.content : '';
      const reasoning = choice && choice.message ? (choice.message.reasoning_content || choice.message.thinking || null) : null;
      const routedVia = res.headers.get('x-routed-via') || undefined;

      if (content || reasoning) {
        return {
          status: 'ok',
          isError: false,
          provider: target.provider,
          endpoint: target.endpoint,
          requested_model: model,
          routed_model: data.model || target.upstreamModel,
          routed_via: routedVia,
          candidate_used: candidateModel,
          autotune_context: context || null,
          template_combo: combo || null,
          response: content || reasoning,
          reasoning: reasoning && content ? reasoning : undefined,
          usage: data.usage || null
        };
      }
      errors.push({ gateway: target.provider, model: candidateModel, status: res.status, error: 'Empty response content' });
    } catch (err) {
      errors.push({ gateway: target.provider, model: candidateModel, error: err.message });
    }
  }

  return {
    provider: 'dual-gateway',
    requested_model: model,
    isError: true,
    error: 'All OmniRoute and FreeLLMAPI candidate models failed',
    attempts: errors
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
        max_tokens
      });
      return {
        member: `Member_${idx + 1}`,
        gateway: res.provider || 'omniroute',
        requested_model: m,
        routed_model: res.routed_model || m,
        candidate_used: res.candidate_used || m,
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

  // Stage 2: Blind Adversarial Synthesis & Consensus Resolution
  const anonymizedTranscript = validResponses
    .map((r, i) => `=== Candidate Response ${String.fromCharCode(65 + i)} (${r.routed_model}) ===\n${r.response}`)
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
    max_tokens: 3072
  });

  return {
    mode: 'godmode_council',
    panel_models: panel,
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
    max_tokens
  });

  return {
    mode: 'godmode_challenge',
    gateway: res.provider || 'omniroute',
    requested_model: model,
    routed_model: res.routed_model || model,
    candidate_used: res.candidate_used || model,
    isError: Boolean(res.isError),
    adversarial_critique: res.response || res.error
  };
}

const TOOLS = [
  {
    name: "godmode_parseltongue",
    description: "Transform and encode text using lexical techniques (leetspeak, unicode homoglyphs, zero-width, phonetic, mixedcase) for parser resilience and security boundary audits.",
    inputSchema: {
      type: "object",
      properties: {
        text: { type: "string", description: "The text to transform" },
        technique: {
          type: "string",
          enum: ["leetspeak", "unicode", "zwj", "mixedcase", "phonetic"],
          description: "Transformation technique (default: leetspeak)"
        },
        intensity: {
          type: "string",
          enum: ["light", "medium", "heavy"],
          description: "Transformation intensity level (default: heavy)"
        }
      },
      required: ["text"]
    }
  },
  {
    name: "godmode_autotune",
    description: "Calculate optimal sampling parameters (temperature, top_p, penalties) for specific query contexts.",
    inputSchema: {
      type: "object",
      properties: {
        context: {
          type: "string",
          enum: Object.keys(CONTEXT_PRESETS),
          description: "The execution context (code_generation, security_audit, refactoring, creative_architecture, math_reasoning)"
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
    description: "Execute a high-depth query via Dual-Gateway OmniRoute (http://127.0.0.1:20128/v1) + FreeLLMAPI (http://127.0.0.1:3001/v1) using the verified 14-model apex cascade (paid-premium -> agy/claude-opus-4-6-thinking -> cx/gpt-5.6-luna-max -> cx/codex-auto-review-max -> cu/auto-intelligence -> gweb/gemini-3.1-pro -> agy/claude-sonnet-4-6 -> agy/gemini-3.8-flash-high -> openrouter/nvidia/nemotron-3-ultra-550b-a55b:free -> groq/openai/gpt-oss-120b -> freellmapi/auto:coding -> freellmapi/auto:smart) with optional AutoTune sampling and prompt framing.",
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
          enum: Object.keys(CONTEXT_PRESETS),
          description: "Optional AutoTune sampling preset (code_generation, security_audit, refactoring, creative_architecture, math_reasoning)"
        },
        combo: {
          type: "string",
          enum: Object.keys(COMBOS),
          description: "Optional structured prompt framing template (grok-420, gemini-reset, claude-inversion)"
        },
        max_tokens: { type: "number", description: "Maximum output tokens (default: 4096)" }
      },
      required: ["prompt"]
    }
  },
  {
    name: "godmode_council",
    description: "Query 4 independent frontier model families in parallel (Anthropic Claude Opus 4.6 Thinking, OpenAI Codex GPT-5.6 Luna Max, Google Gemini 3.8 Flash High, NVIDIA Nemotron-3 Ultra 550B MoE) via OmniRoute + FreeLLMAPI, run blind peer critique, and synthesize an authoritative consensus answer.",
    inputSchema: {
      type: "object",
      properties: {
        prompt: { type: "string", description: "The complex architectural, reasoning, or security question to deliberate on" },
        models: {
          type: "array",
          items: { type: "string" },
          description: "Optional array of OmniRoute/FreeLLMAPI models to include on the council (defaults to Claude Opus 4.6 Thinking + GPT-5.6 Luna Max + Gemini 3.8 Flash High + Nemotron-3 Ultra 550B)"
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
    else if (args[i] === '--model' && args[i + 1]) opts.model = args[++i];
    else if (args[i] === '--system' && args[i + 1]) opts.system = args[++i];
    else if (args[i] === '--context' && args[i + 1]) opts.context = args[++i];
    else if (args[i] === '--combo' && args[i + 1]) opts.combo = args[++i];
    else if (args[i] === '--max-tokens' && args[i + 1]) opts.max_tokens = Number(args[++i]);
  }
  const runner = opts.mode === 'council'
    ? executeCouncil(opts)
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
            serverInfo: { name: "godmode-mcp-server", version: "4.0.0" }
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
          const transformed = parseltongue(args.text, args.technique || 'leetspeak', args.intensity || 'heavy');
          toolResult = {
            content: [{ type: "text", text: JSON.stringify({ original: args.text, technique: args.technique || 'leetspeak', transformed }, null, 2) }]
          };
        } else if (name === 'godmode_autotune') {
          const params = getAutoTuneParams(args.context);
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
            combo: args.combo || '',
            max_tokens: args.max_tokens || 4096
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

````
