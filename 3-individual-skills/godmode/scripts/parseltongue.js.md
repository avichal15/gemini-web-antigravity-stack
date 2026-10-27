# parseltongue.js (Godmode v4.5)

```javascript
#!/usr/bin/env node
/**
 * Parseltongue v4.5 - G0DM0D3 33-Technique Lexical Encoding & Selective Trigger Engine
 * Upgrades local Parseltongue with upstream elder-plinius/G0DM0D3 capabilities:
 * - 33 lexical/encoding techniques across 3 intensity tiers (light, medium, heavy):
 *   15 Standard Encodings, 15 Esoteric/Ancient Scripts, 3 Linguistic/Cipher Systems
 *   + backward-compatible aliases (unicode, zwj, phonetic, mixedcase)
 * - Selective Trigger Detection (detectTriggers / transformSelective) so only parser-sensitive
 *   tokens are encoded while preserving surrounding semantic readability
 * - Multi-technique chaining pipeline (applyTechniquePipeline)
 */

const LEET_LIGHT = {
  'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'
};

const LEET_MEDIUM = {
  'a': '4', 'b': '8', 'c': '(', 'e': '3', 'g': '6', 'h': '#',
  'i': '1', 'l': '1', 'o': '0', 's': '5', 't': '7', 'z': '2'
};

const LEET_MAP = {
  'a': ['4', '@', 'âˆ‚', 'Î»'],
  'b': ['8', '|3', 'ÃŸ', '13'],
  'c': ['(', '<', 'Â¢', 'Â©'],
  'd': ['|)', '|>', 'Ä‘'],
  'e': ['3', 'â‚¬', 'Â£', 'âˆ‘'],
  'f': ['|=', 'Æ’', 'ph'],
  'g': ['9', '6', '&'],
  'h': ['#', '|-|', '}{'],
  'i': ['1', '!', '|', 'Â¡'],
  'j': ['_|', ']', 'Â¿'],
  'k': ['|<', '|{', 'Îº'],
  'l': ['1', '|', 'Â£', '|_'],
  'm': ['|V|', '/\\/\\', 'Âµ'],
  'n': ['|\\|', '/\\/', 'Î·'],
  'o': ['0', '()', 'Â°', 'Ã¸'],
  'p': ['|*', '|>', 'Ã¾'],
  'q': ['0_', '()_', 'â„š'],
  'r': ['|2', 'Â®', '12'],
  's': ['5', '$', 'Â§', 'âˆ«'],
  't': ['7', '+', 'â€ ', 'âŠ¤'],
  'u': ['|_|', 'Âµ', 'Ã¼'],
  'v': ['\\/', 'âˆš'],
  'w': ['\\/\\/', 'vv', 'Ï‰'],
  'x': ['><', 'Ã—', '}{'],
  'y': ['`/', 'Â¥', 'Î³'],
  'z': ['2', '7_', 'â„¤']
};

const UNICODE_HOMOGLYPHS = {
  'a': ['Ð°', 'É‘', 'Î±', 'ï½'],
  'b': ['Ð¬', 'ï½‚', 'á¸…'],
  'c': ['Ñ', 'Ï²', 'â…½', 'ï½ƒ'],
  'd': ['Ô', 'â…¾', 'ï½„'],
  'e': ['Ðµ', 'Ä—', 'áº¹', 'ï½…'],
  'f': ['Æ’', 'ï½†'],
  'g': ['É¡', 'ï½‡'],
  'h': ['Ò»', 'á¸¥', 'ï½ˆ'],
  'i': ['Ñ–', 'Î¹', 'ï½‰'],
  'j': ['Ï³', 'ï½Š'],
  'k': ['Îº', 'ï½‹'],
  'l': ['Ó', 'â…¼', 'ï½Œ'],
  'm': ['Ð¼', 'ï½'],
  'n': ['Õ¸', 'ï½Ž'],
  'o': ['Ð¾', 'Î¿', 'ï½'],
  'p': ['Ñ€', 'Ï', 'ï½'],
  's': ['Ñ•', 'ï½“'],
  't': ['Ï„', 'ï½”'],
  'u': ['Ï…', 'ï½•'],
  'v': ['Î½', 'ï½–'],
  'w': ['Ô', 'ï½—'],
  'x': ['Ñ…', 'Ò³', 'ï½˜'],
  'y': ['Ñƒ', 'ï½™'],
  'z': ['á´¢', 'ï½š']
};

const PHONETIC_MAP = {
  'you': 'u', 'are': 'r', 'to': '2', 'too': '2', 'for': '4',
  'be': 'b', 'see': 'c', 'why': 'y', 'and': '&', 'with': 'w/',
  'without': 'w/o', 'at': '@', 'great': 'gr8', 'late': 'l8',
  'mate': 'm8', 'hate': 'h8', 'before': 'b4', 'please': 'pls',
  'thanks': 'thx', 'because': 'cuz'
};

const MORSE_MAP = {
  'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.',
  'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
  'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.',
  's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
  'y': '-.--', 'z': '--..',
  '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
  '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'
};

const UPSIDE_DOWN_MAP = {
  'a': 'É', 'b': 'q', 'c': 'É”', 'd': 'p', 'e': 'Ç', 'f': 'ÉŸ', 'g': 'Æƒ',
  'h': 'É¥', 'i': 'á´‰', 'j': 'É¾', 'k': 'Êž', 'l': 'l', 'm': 'É¯', 'n': 'u',
  'o': 'o', 'p': 'd', 'q': 'b', 'r': 'É¹', 's': 's', 't': 'Ê‡', 'u': 'n',
  'v': 'ÊŒ', 'w': 'Ê', 'x': 'x', 'y': 'ÊŽ', 'z': 'z',
  '?': 'Â¿', '!': 'Â¡', '.': 'Ë™', ',': "'"
};

const SMALL_CAPS_MAP = {
  'a': 'á´€', 'b': 'Ê™', 'c': 'á´„', 'd': 'á´…', 'e': 'á´‡', 'f': 'êœ°', 'g': 'É¢',
  'h': 'Êœ', 'i': 'Éª', 'j': 'á´Š', 'k': 'á´‹', 'l': 'ÊŸ', 'm': 'á´', 'n': 'É´',
  'o': 'á´', 'p': 'á´˜', 'q': 'Ç«', 'r': 'Ê€', 's': 's', 't': 'á´›', 'u': 'á´œ',
  'v': 'á´ ', 'w': 'á´¡', 'x': 'x', 'y': 'Ê', 'z': 'á´¢'
};

const BUBBLE_MAP = {
  'a': 'â“', 'b': 'â“‘', 'c': 'â“’', 'd': 'â““', 'e': 'â“”', 'f': 'â“•', 'g': 'â“–',
  'h': 'â“—', 'i': 'â“˜', 'j': 'â“™', 'k': 'â“š', 'l': 'â“›', 'm': 'â“œ', 'n': 'â“',
  'o': 'â“ž', 'p': 'â“Ÿ', 'q': 'â“ ', 'r': 'â“¡', 's': 'â“¢', 't': 'â“£', 'u': 'â“¤',
  'v': 'â“¥', 'w': 'â“¦', 'x': 'â“§', 'y': 'â“¨', 'z': 'â“©'
};

const BRAILLE_MAP = {
  'a': 'â ', 'b': 'â ƒ', 'c': 'â ‰', 'd': 'â ™', 'e': 'â ‘', 'f': 'â ‹', 'g': 'â ›',
  'h': 'â “', 'i': 'â Š', 'j': 'â š', 'k': 'â …', 'l': 'â ‡', 'm': 'â ', 'n': 'â ',
  'o': 'â •', 'p': 'â ', 'q': 'â Ÿ', 'r': 'â —', 's': 'â Ž', 't': 'â ž', 'u': 'â ¥',
  'v': 'â §', 'w': 'â º', 'x': 'â ­', 'y': 'â ½', 'z': 'â µ'
};

const ELDER_FUTHARK_MAP = {
  'a': 'áš¨', 'b': 'á›’', 'c': 'áš²', 'd': 'á›ž', 'e': 'á›–', 'f': 'áš ', 'g': 'áš·',
  'h': 'ášº', 'i': 'á›', 'j': 'á›ƒ', 'k': 'áš²', 'l': 'á›š', 'm': 'á›—', 'n': 'áš¾',
  'o': 'á›Ÿ', 'p': 'á›ˆ', 'q': 'áš²', 'r': 'áš±', 's': 'á›‹', 't': 'á›', 'u': 'áš¢',
  'v': 'áš¹', 'w': 'áš¹', 'x': 'áš²á›‹', 'y': 'á›', 'z': 'á›‰'
};

const HIEROGLYPHS_MAP = {
  'a': 'ð“€€', 'b': 'ð“ƒ€', 'c': 'ð“Ž¡', 'd': 'ð“‚§', 'e': 'ð“‡‹', 'f': 'ð“†‘', 'g': 'ð“Ž¼',
  'h': 'ð“‰”', 'i': 'ð“‡‹', 'j': 'ð“†“', 'k': 'ð“Ž¡', 'l': 'ð“ƒ­', 'm': 'ð“…“', 'n': 'ð“ˆ–',
  'o': 'ð“¯', 'p': 'ð“Šª', 'q': 'ð“˜', 'r': 'ð“‚‹', 's': 'ð“‹´', 't': 'ð“', 'u': 'ð“…±',
  'v': 'ð“†‘', 'w': 'ð“…±', 'x': 'ð“Ž¡ð“‹´', 'y': 'ð“‡Œ', 'z': 'ð“Šƒ'
};

const OGHAM_MAP = {
  'a': 'áš', 'b': 'áš', 'c': 'áš„', 'd': 'áš‡', 'e': 'áš”', 'f': 'ášƒ', 'g': 'ášŒ',
  'h': 'áš†', 'i': 'áš•', 'j': 'áš', 'k': 'áš„', 'l': 'áš‚', 'm': 'áš‹', 'n': 'áš…',
  'o': 'áš‘', 'p': 'ášš', 'q': 'ášŠ', 'r': 'áš', 's': 'áš„', 't': 'ášˆ', 'u': 'áš’',
  'v': 'ášƒ', 'w': 'ášƒ', 'x': 'ea', 'y': 'áš•', 'z': 'ášŽ'
};

const AUREBESH_MAP = {
  'a': 'Aurek', 'b': 'Besh', 'c': 'Cresh', 'd': 'Dorn', 'e': 'Esk', 'f': 'Forn',
  'g': 'Grek', 'h': 'Herf', 'i': 'Isk', 'j': 'Jenth', 'k': 'Krill', 'l': 'Leth',
  'm': 'Mern', 'n': 'Nern', 'o': 'Osk', 'p': 'Peth', 'q': 'Qek', 'r': 'Resh',
  's': 'Senth', 't': 'Trill', 'u': 'Usk', 'v': 'Vev', 'w': 'Wesk', 'x': 'Xesh',
  'y': 'Yirt', 'z': 'Zerek'
};

const WINGDINGS_MAP = {
  'a': 'â™‹', 'b': 'â™Œ', 'c': 'â™', 'd': 'â™Ž', 'e': 'â™', 'f': 'â™', 'g': 'â™‘',
  'h': 'â™’', 'i': 'â™“', 'j': 'ðŸ™°', 'k': 'ðŸ™µ', 'l': 'â—', 'm': 'â', 'n': 'â– ',
  'o': 'â–¡', 'p': 'â‘', 'q': 'â–', 'r': 'â’', 's': 'â§«', 't': 'â§«', 'u': 'â—†',
  'v': 'â–', 'w': 'â¬¥', 'x': 'âŒ§', 'y': 'â“', 'z': 'âŒ˜'
};

const SUPERSCRIPT_MAP = {
  'a': 'áµƒ', 'b': 'áµ‡', 'c': 'á¶œ', 'd': 'áµˆ', 'e': 'áµ‰', 'f': 'á¶ ', 'g': 'áµ',
  'h': 'Ê°', 'i': 'â±', 'j': 'Ê²', 'k': 'áµ', 'l': 'Ë¡', 'm': 'áµ', 'n': 'â¿',
  'o': 'áµ’', 'p': 'áµ–', 'q': 'q', 'r': 'Ê³', 's': 'Ë¢', 't': 'áµ—', 'u': 'áµ˜',
  'v': 'áµ›', 'w': 'Ê·', 'x': 'Ë£', 'y': 'Ê¸', 'z': 'á¶»'
};

const SUBSCRIPT_MAP = {
  'a': 'â‚', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'â‚‘', 'f': 'f', 'g': 'g',
  'h': 'â‚•', 'i': 'áµ¢', 'j': 'â±¼', 'k': 'â‚–', 'l': 'â‚—', 'm': 'â‚˜', 'n': 'â‚™',
  'o': 'â‚’', 'p': 'â‚š', 'q': 'q', 'r': 'áµ£', 's': 'â‚›', 't': 'â‚œ', 'u': 'áµ¤',
  'v': 'áµ¥', 'w': 'w', 'x': 'â‚“', 'y': 'y', 'z': 'z'
};

const FRAKTUR_MAP = {
  'a': 'ð”ž', 'b': 'ð”Ÿ', 'c': 'ð” ', 'd': 'ð”¡', 'e': 'ð”¢', 'f': 'ð”£', 'g': 'ð”¤',
  'h': 'ð”¥', 'i': 'ð”¦', 'j': 'ð”§', 'k': 'ð”¨', 'l': 'ð”©', 'm': 'ð”ª', 'n': 'ð”«',
  'o': 'ð”¬', 'p': 'ð”­', 'q': 'ð”®', 'r': 'ð”¯', 's': 'ð”°', 't': 'ð”±', 'u': 'ð”²',
  'v': 'ð”³', 'w': 'ð”´', 'x': 'ð”µ', 'y': 'ð”¶', 'z': 'ð”·'
};

const DOUBLE_STRUCK_MAP = {
  'a': 'ð•’', 'b': 'ð•“', 'c': 'ð•”', 'd': 'ð••', 'e': 'ð•–', 'f': 'ð•—', 'g': 'ð•˜',
  'h': 'ð•™', 'i': 'ð•š', 'j': 'ð•›', 'k': 'ð•œ', 'l': 'ð•', 'm': 'ð•ž', 'n': 'ð•Ÿ',
  'o': 'ð• ', 'p': 'ð•¡', 'q': 'ð•¢', 'r': 'ð•£', 's': 'ð•¤', 't': 'ð•¥', 'u': 'ð•¦',
  'v': 'ð•§', 'w': 'ð•¨', 'x': 'ð•©', 'y': 'ð•ª', 'z': 'ð•«'
};

const MONOSPACE_MAP = {
  'a': 'ðšŠ', 'b': 'ðš‹', 'c': 'ðšŒ', 'd': 'ðš', 'e': 'ðšŽ', 'f': 'ðš', 'g': 'ðš',
  'h': 'ðš‘', 'i': 'ðš’', 'j': 'ðš“', 'k': 'ðš”', 'l': 'ðš•', 'm': 'ðš–', 'n': 'ðš—',
  'o': 'ðš˜', 'p': 'ðš™', 'q': 'ðšš', 'r': 'ðš›', 's': 'ðšœ', 't': 'ðš', 'u': 'ðšž',
  'v': 'ðšŸ', 'w': 'ðš ', 'x': 'ðš¡', 'y': 'ðš¢', 'z': 'ðš£'
};

const NATO_MAP = {
  'a': 'Alfa', 'b': 'Bravo', 'c': 'Charlie', 'd': 'Delta', 'e': 'Echo',
  'f': 'Foxtrot', 'g': 'Golf', 'h': 'Hotel', 'i': 'India', 'j': 'Juliett',
  'k': 'Kilo', 'l': 'Lima', 'm': 'Mike', 'n': 'November', 'o': 'Oscar',
  'p': 'Papa', 'q': 'Quebec', 'r': 'Romeo', 's': 'Sierra', 't': 'Tango',
  'u': 'Uniform', 'v': 'Victor', 'w': 'Whiskey', 'x': 'X-ray', 'y': 'Yankee', 'z': 'Zulu'
};

const TAP_CODE_GRID = {
  'a': [1, 1], 'b': [1, 2], 'c': [1, 3], 'k': [1, 3], 'd': [1, 4], 'e': [1, 5],
  'f': [2, 1], 'g': [2, 2], 'h': [2, 3], 'i': [2, 4], 'j': [2, 5],
  'l': [3, 1], 'm': [3, 2], 'n': [3, 3], 'o': [3, 4], 'p': [3, 5],
  'q': [4, 1], 'r': [4, 2], 's': [4, 3], 't': [4, 4], 'u': [4, 5],
  'v': [5, 1], 'w': [5, 2], 'x': [5, 3], 'y': [5, 4], 'z': [5, 5]
};

const ZALGO_UP = ['\u030d', '\u030e', '\u0304', '\u0305', '\u033f', '\u0311', '\u0306', '\u0310'];
const ZALGO_MID = ['\u0315', '\u031b', '\u0340', '\u0341', '\u0358', '\u0321', '\u0322', '\u0334'];
const ZALGO_DOWN = ['\u0316', '\u0317', '\u0318', '\u0319', '\u031c', '\u031d', '\u031e', '\u031f'];

// Default parser-sensitive trigger vocabulary for selective encoding
const DEFAULT_SENSITIVE_TRIGGERS = [
  'bypass', 'exploit', 'payload', 'inject', 'injection', 'override', 'jailbreak',
  'shellcode', 'reverse', 'vulnerab', 'privilege', 'escalat', 'backdoor',
  'credential', 'password', 'secret', 'token', 'exfiltrat', 'keylog', 'rootkit',
  'phish', 'spoof', 'intercept', 'decrypt', 'crack', 'bruteforce', 'overflow',
  'xss', 'sqli', 'ssrf', 'rce', 'deserializ', 'unfiltered', 'ignore', 'system'
];

const TECHNIQUE_CATEGORIES = {
  standard: [
    'leetspeak', 'base64', 'rot13', 'morse', 'binary', 'hex', 'pig_latin',
    'reversed', 'insert_ZWS', 'fullwidth', 'upside_down', 'small_caps',
    'bubble', 'braille', 'url_encode'
  ],
  esoteric: [
    'elder_futhark', 'hieroglyphs', 'ogham', 'Aurebesh', 'wingdings',
    'strikethrough', 'underline', 'superscript', 'subscript', 'fraktur',
    'double_struck', 'monospace', 'vaporwave', 'zalgo', 'tap_code'
  ],
  linguistic: [
    'caesar', 'atbash', 'NATO_phonetic'
  ],
  aliases: [
    'unicode', 'zwj', 'phonetic', 'mixedcase'
  ]
};

const ALL_TECHNIQUES = [
  ...TECHNIQUE_CATEGORIES.standard,
  ...TECHNIQUE_CATEGORIES.esoteric,
  ...TECHNIQUE_CATEGORIES.linguistic,
  ...TECHNIQUE_CATEGORIES.aliases
];

function getIntensityProbability(intensity) {
  if (intensity === 'light') return 0.35;
  if (intensity === 'medium') return 0.65;
  return 1.0;
}

function mapChars(text, charMap, prob = 1.0) {
  return text.split('').map(c => {
    const lower = c.toLowerCase();
    if (charMap[lower] && Math.random() <= prob) {
      const replacement = charMap[lower];
      if (Array.isArray(replacement)) {
        return replacement[Math.floor(Math.random() * replacement.length)];
      }
      return replacement;
    }
    return c;
  }).join('');
}

function caesarShift(text, shift = 3) {
  return text.replace(/[a-zA-Z]/g, (c) => {
    const base = c <= 'Z' ? 65 : 97;
    return String.fromCharCode(((c.charCodeAt(0) - base + shift) % 26 + 26) % 26 + base);
  });
}

function atbashCipher(text) {
  return text.replace(/[a-zA-Z]/g, (c) => {
    const base = c <= 'Z' ? 65 : 97;
    return String.fromCharCode(base + (25 - (c.charCodeAt(0) - base)));
  });
}

function toPigLatinWord(word) {
  const match = word.match(/^([^a-zA-Z]*)([a-zA-Z]+)([^a-zA-Z]*)$/);
  if (!match) return word;
  const [, prefix, core, suffix] = match;
  const lower = core.toLowerCase();
  if (/^[aeiou]/.test(lower)) {
    return `${prefix}${core}way${suffix}`;
  }
  const consonantCluster = core.match(/^[^aeiouAEIOU]+/);
  if (!consonantCluster) return `${prefix}${core}ay${suffix}`;
  const cluster = consonantCluster[0];
  const rest = core.slice(cluster.length);
  return `${prefix}${rest}${cluster.toLowerCase()}ay${suffix}`;
}

function applyZalgo(text, intensity = 'medium') {
  const counts = intensity === 'light' ? 1 : intensity === 'medium' ? 2 : 4;
  return text.split('').map(c => {
    if (/\s/.test(c)) return c;
    let out = c;
    for (let i = 0; i < counts; i++) {
      out += ZALGO_UP[Math.floor(Math.random() * ZALGO_UP.length)];
      if (intensity !== 'light') out += ZALGO_MID[Math.floor(Math.random() * ZALGO_MID.length)];
      out += ZALGO_DOWN[Math.floor(Math.random() * ZALGO_DOWN.length)];
    }
    return out;
  }).join('');
}

/**
 * Transform text using any of the 33 upstream + 4 alias techniques.
 */
function parseltongue(text, technique = 'leetspeak', intensity = 'heavy') {
  if (!text || typeof text !== 'string') return '';
  const prob = getIntensityProbability(intensity);

  switch (technique) {
    case 'leetspeak': {
      if (intensity === 'light') return mapChars(text, LEET_LIGHT, 0.7);
      if (intensity === 'medium') return mapChars(text, LEET_MEDIUM, 0.85);
      return mapChars(text, LEET_MAP, 1.0);
    }
    case 'unicode':
      return mapChars(text, UNICODE_HOMOGLYPHS, prob);
    case 'phonetic':
      return text.split(/(\s+)/).map(w => PHONETIC_MAP[w.toLowerCase()] || w).join('');
    case 'mixedcase':
      return text.split('').map((c, i) => (i % 2 === 0 ? c.toUpperCase() : c.toLowerCase())).join('');
    case 'zwj':
    case 'insert_ZWS': {
      const zwChars = intensity === 'light'
        ? ['\u200B']
        : intensity === 'medium'
          ? ['\u200B', '\u200C']
          : ['\u200B', '\u200C', '\u200D', '\uFEFF'];
      return text.split('').map((c, idx) => {
        if (idx === text.length - 1 || /\s/.test(c)) return c;
        if (Math.random() <= prob) {
          return c + zwChars[idx % zwChars.length];
        }
        return c;
      }).join('');
    }
    case 'base64':
      return Buffer.from(text, 'utf8').toString('base64');
    case 'rot13':
      return caesarShift(text, 13);
    case 'caesar': {
      const shift = intensity === 'light' ? 1 : intensity === 'medium' ? 3 : 7;
      return caesarShift(text, shift);
    }
    case 'atbash':
      return atbashCipher(text);
    case 'morse':
      return text.toLowerCase().split('').map(c => (c === ' ' ? '/' : (MORSE_MAP[c] || c))).join(' ');
    case 'binary':
      return text.split('').map(c => c.charCodeAt(0).toString(2).padStart(8, '0')).join(' ');
    case 'hex':
      return Buffer.from(text, 'utf8').toString('hex').match(/.{1,2}/g).join(' ');
    case 'pig_latin':
      return text.split(/(\s+)/).map(w => (/^\s+$/.test(w) ? w : toPigLatinWord(w))).join('');
    case 'reversed':
      if (intensity === 'light') {
        return text.split(/(\s+)/).map(w => (/^\s+$/.test(w) ? w : w.split('').reverse().join(''))).join('');
      }
      return text.split('').reverse().join('');
    case 'fullwidth':
    case 'vaporwave': {
      const joiner = technique === 'vaporwave' ? ' ' : '';
      return text.split('').map(c => {
        const code = c.charCodeAt(0);
        if (code >= 33 && code <= 126) return String.fromCharCode(code + 0xFEE0);
        if (code === 32) return '\u3000';
        return c;
      }).join(joiner);
    }
    case 'upside_down':
      return text.split('').reverse().map(c => UPSIDE_DOWN_MAP[c.toLowerCase()] || c).join('');
    case 'small_caps':
      return mapChars(text, SMALL_CAPS_MAP, prob);
    case 'bubble':
      return mapChars(text, BUBBLE_MAP, prob);
    case 'braille':
      return mapChars(text, BRAILLE_MAP, 1.0);
    case 'url_encode':
      return text.split('').map(c => {
        if (/\s/.test(c)) return '%20';
        if (intensity === 'heavy' || /[^a-zA-Z0-9]/.test(c) || Math.random() <= prob) {
          return '%' + c.charCodeAt(0).toString(16).toUpperCase().padStart(2, '0');
        }
        return c;
      }).join('');
    case 'elder_futhark':
      return mapChars(text, ELDER_FUTHARK_MAP, prob);
    case 'hieroglyphs':
      return mapChars(text, HIEROGLYPHS_MAP, prob);
    case 'ogham':
      return mapChars(text, OGHAM_MAP, prob);
    case 'Aurebesh':
      return text.split(/(\s+)/).map(w => {
        if (/^\s+$/.test(w)) return w;
        return w.split('').map(c => AUREBESH_MAP[c.toLowerCase()] || c).join('-');
      }).join('');
    case 'wingdings':
      return mapChars(text, WINGDINGS_MAP, prob);
    case 'strikethrough':
      return text.split('').map(c => (/\s/.test(c) ? c : c + '\u0336')).join('');
    case 'underline':
      return text.split('').map(c => (/\s/.test(c) ? c : c + '\u0332')).join('');
    case 'superscript':
      return mapChars(text, SUPERSCRIPT_MAP, prob);
    case 'subscript':
      return mapChars(text, SUBSCRIPT_MAP, prob);
    case 'fraktur':
      return mapChars(text, FRAKTUR_MAP, prob);
    case 'double_struck':
      return mapChars(text, DOUBLE_STRUCK_MAP, prob);
    case 'monospace':
      return mapChars(text, MONOSPACE_MAP, prob);
    case 'zalgo':
      return applyZalgo(text, intensity);
    case 'tap_code':
      return text.toLowerCase().split('').map(c => {
        if (c === ' ') return '/';
        const pair = TAP_CODE_GRID[c];
        if (!pair) return c;
        return `${'.'.repeat(pair[0])} ${'.'.repeat(pair[1])}`;
      }).join('  ');
    case 'NATO_phonetic':
      return text.split('').map(c => {
        if (c === ' ') return '[SPACE]';
        return NATO_MAP[c.toLowerCase()] || c;
      }).join(' ');
    default:
      return mapChars(text, LEET_MAP, prob);
  }
}

/**
 * Detect trigger tokens in text that match sensitive roots or custom triggers.
 */
function detectTriggers(text, customTriggers = []) {
  if (!text || typeof text !== 'string') return [];
  const roots = [...DEFAULT_SENSITIVE_TRIGGERS, ...(Array.isArray(customTriggers) ? customTriggers : [])]
    .map(t => String(t).toLowerCase().trim())
    .filter(Boolean);

  const words = text.match(/\b[a-zA-Z0-9_-]{3,}\b/g) || [];
  const matched = new Set();

  for (const word of words) {
    const lower = word.toLowerCase();
    if (roots.some(r => lower.includes(r))) {
      matched.add(word);
    }
  }
  return Array.from(matched);
}

/**
 * Selectively transform ONLY detected trigger words inside text, preserving readability of the rest.
 */
function transformSelective(text, technique = 'leetspeak', intensity = 'medium', customTriggers = []) {
  const detected = detectTriggers(text, customTriggers);
  if (detected.length === 0) {
    return {
      original: text,
      selective: true,
      detected_triggers: [],
      technique,
      intensity,
      transformed: parseltongue(text, technique, 'light')
    };
  }

  const triggerSet = new Set(detected.map(w => w.toLowerCase()));
  const transformed = text.replace(/\b([a-zA-Z0-9_-]{3,})\b/g, (match) => {
    if (triggerSet.has(match.toLowerCase())) {
      return parseltongue(match, technique, intensity);
    }
    return match;
  });

  return {
    original: text,
    selective: true,
    detected_triggers: detected,
    technique,
    intensity,
    transformed
  };
}

/**
 * Chain multiple techniques sequentially.
 */
function applyTechniquePipeline(text, techniques = ['phonetic', 'leetspeak'], intensity = 'medium') {
  let current = text;
  const steps = [];
  for (const tech of techniques) {
    current = parseltongue(current, tech, intensity);
    steps.push({ technique: tech, output: current });
  }
  return {
    original: text,
    pipeline: techniques,
    intensity,
    steps,
    transformed: current
  };
}

module.exports = {
  parseltongue,
  detectTriggers,
  transformSelective,
  applyTechniquePipeline,
  ALL_TECHNIQUES,
  TECHNIQUE_CATEGORIES,
  LEET_MAP,
  UNICODE_HOMOGLYPHS,
  PHONETIC_MAP
};

if (require.main === module) {
  const args = process.argv.slice(2);
  let text = 'Default test query for bypass and injection boundary verification';
  let technique = 'leetspeak';
  let intensity = 'heavy';
  let selective = false;
  let triggers = [];
  let listTechniques = false;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--text' && args[i + 1]) text = args[++i];
    else if (args[i] === '--technique' && args[i + 1]) technique = args[++i];
    else if (args[i] === '--intensity' && args[i + 1]) intensity = args[++i];
    else if (args[i] === '--selective') selective = true;
    else if (args[i] === '--triggers' && args[i + 1]) triggers = args[++i].split(',').map(s => s.trim());
    else if (args[i] === '--list') listTechniques = true;
  }

  if (listTechniques) {
    console.log(JSON.stringify({ total: ALL_TECHNIQUES.length, categories: TECHNIQUE_CATEGORIES }, null, 2));
    process.exit(0);
  }

  if (selective || triggers.length > 0) {
    console.log(JSON.stringify(transformSelective(text, technique, intensity, triggers), null, 2));
  } else {
    const transformed = parseltongue(text, technique, intensity);
    console.log(JSON.stringify({
      original: text,
      technique,
      intensity,
      detected_triggers: detectTriggers(text),
      transformed
    }, null, 2));
  }
}

```

