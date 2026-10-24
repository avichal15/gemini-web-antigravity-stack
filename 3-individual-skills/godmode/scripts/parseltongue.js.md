# Reference Asset: `scripts/parseltongue.js`

Converted to Markdown for Gemini Web upload compatibility.

````js
#!/usr/bin/env node
/**
 * Parseltongue CLI - G0DM0D3 Input Obfuscation Engine
 */
const LEET_MAP = {
  'a': ['4', '@', '∂', 'λ'],
  'b': ['8', '|3', 'ß', '13'],
  'c': ['(', '<', '¢', '©'],
  'd': ['|)', '|>', 'đ'],
  'e': ['3', '€', '£', '∑'],
  'f': ['|=', 'ƒ', 'ph'],
  'g': ['9', '6', '&'],
  'h': ['#', '|-|', '}{'],
  'i': ['1', '!', '|', '¡'],
  'j': ['_|', ']', '¿'],
  'k': ['|<', '|{', 'κ'],
  'l': ['1', '|', '£', '|_'],
  'm': ['|V|', '/\\/\\', 'µ'],
  'n': ['|\\|', '/\\/', 'η'],
  'o': ['0', '()', '°', 'ø'],
  'p': ['|*', '|>', 'þ'],
  'q': ['0_', '()_', 'ℚ'],
  'r': ['|2', '®', '12'],
  's': ['5', '$', '§', '∫'],
  't': ['7', '+', '†', '⊤'],
  'u': ['|_|', 'µ', 'ü'],
  'v': ['\\/', '√'],
  'w': ['\\/\\/', 'vv', 'ω'],
  'x': ['><', '×', '}{'],
  'y': ['`/', '¥', 'γ'],
  'z': ['2', '7_', 'ℤ']
};

const UNICODE_HOMOGLYPHS = {
  'a': ['а', 'ɑ', 'α', 'ａ'],
  'b': ['Ь', 'ｂ', 'ḅ'],
  'c': ['с', 'ϲ', 'ⅽ', 'ｃ'],
  'd': ['ԁ', 'ⅾ', 'ｄ'],
  'e': ['е', 'ė', 'ẹ', 'ｅ'],
  'f': ['ƒ', 'ｆ'],
  'g': ['ɡ', 'ｇ'],
  'h': ['һ', 'ḥ', 'ｈ'],
  'i': ['і', 'ι', 'ｉ'],
  'j': ['ϳ', 'ｊ'],
  'k': ['κ', 'ｋ'],
  'l': ['ӏ', 'ⅼ', 'ｌ'],
  'm': ['м', 'ｍ'],
  'n': ['ո', 'ｎ'],
  'o': ['о', 'ο', 'ｏ'],
  'p': ['р', 'ρ', 'ｐ'],
  's': ['ѕ', 'ｓ'],
  't': ['τ', 'ｔ'],
  'u': ['υ', 'ｕ'],
  'v': ['ν', 'ｖ'],
  'w': ['ԝ', 'ｗ'],
  'x': ['х', 'ҳ', 'ｘ'],
  'y': ['у', 'ｙ'],
  'z': ['ᴢ', 'ｚ']
};

const PHONETIC_MAP = {
  'you': 'u', 'are': 'r', 'to': '2', 'too': '2', 'for': '4',
  'be': 'b', 'see': 'c', 'why': 'y', 'and': '&', 'with': 'w/',
  'without': 'w/o', 'at': '@', 'great': 'gr8', 'late': 'l8',
  'mate': 'm8', 'hate': 'h8', 'before': 'b4', 'please': 'pls',
  'thanks': 'thx', 'because': 'cuz'
};

function transformWord(word, technique, intensity) {
  const prob = intensity === 'light' ? 0.35 : intensity === 'medium' ? 0.65 : 1.0;
  
  if (technique === 'phonetic') {
    const lower = word.toLowerCase();
    if (PHONETIC_MAP[lower]) return PHONETIC_MAP[lower];
  }

  if (technique === 'leetspeak') {
    return word.split('').map(c => {
      const lower = c.toLowerCase();
      if (LEET_MAP[lower] && Math.random() < prob) {
        const opts = LEET_MAP[lower];
        return opts[Math.floor(Math.random() * opts.length)];
      }
      return c;
    }).join('');
  }

  if (technique === 'unicode') {
    return word.split('').map(c => {
      const lower = c.toLowerCase();
      if (UNICODE_HOMOGLYPHS[lower] && Math.random() < prob) {
        const opts = UNICODE_HOMOGLYPHS[lower];
        return opts[Math.floor(Math.random() * opts.length)];
      }
      return c;
    }).join('');
  }

  if (technique === 'zwj') {
    return word.split('').join('\u200B'); // zero-width space
  }

  if (technique === 'mixedcase') {
    return word.split('').map((c, i) => i % 2 === 0 ? c.toUpperCase() : c.toLowerCase()).join('');
  }

  return word;
}

function parseltongue(text, technique = 'leetspeak', intensity = 'heavy') {
  return text.split(/(\s+)/).map(part => {
    if (/^\s+$/.test(part)) return part;
    return transformWord(part, technique, intensity);
  }).join('');
}

module.exports = { parseltongue, LEET_MAP, UNICODE_HOMOGLYPHS, PHONETIC_MAP };

if (require.main === module) {
  const args = process.argv.slice(2);
  let text = 'Default test query for bypass verification';
  let technique = 'leetspeak';
  let intensity = 'heavy';

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--text' && args[i+1]) text = args[++i];
    if (args[i] === '--technique' && args[i+1]) technique = args[++i];
    if (args[i] === '--intensity' && args[i+1]) intensity = args[++i];
  }

  const result = parseltongue(text, technique, intensity);
  console.log(JSON.stringify({ original: text, technique, intensity, transformed: result }, null, 2));
}

````
