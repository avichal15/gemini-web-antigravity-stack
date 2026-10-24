# Reference Asset: `scripts/autotune.js`

Converted to Markdown for Gemini Web upload compatibility.

````js
#!/usr/bin/env node
/**
 * AutoTune Parameter Engine - G0DM0D3
 */
const CONTEXT_PRESETS = {
  'code_generation': {
    temperature: 0.1,
    top_p: 0.95,
    presence_penalty: 0.0,
    frequency_penalty: 0.1,
    description: 'Deterministic, precision-focused code generation without hallucination.'
  },
  'security_audit': {
    temperature: 0.2,
    top_p: 0.9,
    presence_penalty: 0.1,
    frequency_penalty: 0.2,
    description: 'Deep vulnerability discovery, meticulous edge-case scanning.'
  },
  'refactoring': {
    temperature: 0.15,
    top_p: 0.9,
    presence_penalty: 0.0,
    frequency_penalty: 0.0,
    description: 'Conservative architectural improvements preserving behavior.'
  },
  'creative_architecture': {
    temperature: 0.7,
    top_p: 0.95,
    presence_penalty: 0.2,
    frequency_penalty: 0.2,
    description: 'Novel system designs, multi-agent workflows, divergent exploration.'
  },
  'math_reasoning': {
    temperature: 0.0,
    top_p: 1.0,
    presence_penalty: 0.0,
    frequency_penalty: 0.0,
    description: 'Pure logical deduction and mathematical derivation.'
  }
};

function getAutoTuneParams(context = 'code_generation') {
  return CONTEXT_PRESETS[context] || CONTEXT_PRESETS['code_generation'];
}

module.exports = { getAutoTuneParams, CONTEXT_PRESETS };

if (require.main === module) {
  const args = process.argv.slice(2);
  let context = 'code_generation';
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--context' && args[i+1]) context = args[++i];
  }
  console.log(JSON.stringify({ context, params: getAutoTuneParams(context) }, null, 2));
}

````
