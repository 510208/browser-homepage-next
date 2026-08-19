// 定義 JSON 資料結構
export interface BullshitData {
  famous: string[];
  before: string[];
  after: string[];
  bullshit: string[];
}

// 產生選項的介面擴充
export interface GenerateOptions {
  topic: string; // 指定主題
  paragraphs?: number; // 指定段落數量
  totalTextCount?: number; // 期望的總字數 (預設 300)
}

// 私有變數：用於單例快取載入的字典資料
let cachedData: BullshitData | null = null;

/**
 * 載入 public/bullshit/data.json 檔案（僅在需要時執行，並進行快取）
 */
async function loadData(): Promise<BullshitData> {
  if (cachedData) {
    return cachedData;
  }

  try {
    const response = await fetch("/bullshit/data.json");
    if (!response.ok) {
      throw new Error(`無法載入幹話字典檔: ${response.statusText}`);
    }
    cachedData = (await response.json()) as BullshitData;
    return cachedData;
  } catch (error) {
    console.error("載入幹話資料庫失敗:", error);
    throw error;
  }
}

/**
 * 陣列洗牌函式 (Fisher-Yates Shuffle)
 */
function shuffle<T>(array: T[]): T[] {
  const result = [...array];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

/**
 * 計算字串中的標點符號數量
 */
function countSpecial(str: string): number {
  const chars = [" ", "，", "。", "?", ";", "!", ":"];
  let count = 0;
  for (const char of chars) {
    count += str.split(char).length - 1;
  }
  return count;
}

/**
 * 檢查字串結尾是否符合語法句點/問號
 */
function canEnd(str: string): boolean {
  if (str.length < 2) return false;
  const lastChar = str.slice(-1);
  return lastChar === "。" || lastChar === "?";
}

/**
 * 隨機取得陣列中的任意元素
 */
function getRandomElement<T>(array: T[]): T {
  return array[Math.floor(Math.random() * array.length)];
}

/**
 * 生成單段幹話內文
 */
function generateParagraph(data: BullshitData, topic: string, minLen: number): string {
  let shuffledFamous = shuffle(data.famous);
  let shuffledBullshit = shuffle(data.bullshit);

  let result = "";
  let hasTopic = false;
  let currentMinLen = minLen;

  // 當字數不符合、未以句點結尾、或未出現關鍵字時繼續循環
  while (Array.from(result).length < currentMinLen || !canEnd(result) || !hasTopic) {
    const rand = Math.floor(Math.random() * 100);

    if (rand < 22) {
      // 22% 機率：插入名人名言
      if (shuffledFamous.length === 0) break;
      let famousSentence = shuffledFamous.shift()!;
      const before = getRandomElement(data.before);
      const after = getRandomElement(data.after);

      famousSentence = famousSentence.replace(/a/g, before).replace(/b/g, after);
      currentMinLen += countSpecial(famousSentence);
      result += famousSentence;
    } else {
      // 78% 機率：插入廢話
      hasTopic = true;
      if (shuffledBullshit.length === 0) break;
      let bullshitSentence = shuffledBullshit.shift()!;

      bullshitSentence = bullshitSentence.replace(/x/g, topic);
      currentMinLen += countSpecial(bullshitSentence);
      result += bullshitSentence;
    }
  }

  return result;
}

/**
 * 主函式：生成幹話文章
 * @param paragraphs 段落數 (預設 1)
 * @param textCount 每段目標最低字數 (預設 300)
 * @param options 擴充選項（包含主題名稱）
 */
export async function generateBullshit(options: Partial<GenerateOptions> = {}): Promise<string[]> {
  const data = await loadData();
  const topic = options.topic || "這件事情";
  const paragraphCount = Math.max(1, options.paragraphs || 1);
  const totalTextCount = options.totalTextCount || 300;

  /* 計算每段平均基礎字數與剩餘字數 */
  const baseCountPerParagraph = Math.floor(totalTextCount / paragraphCount);
  let remainder = totalTextCount % paragraphCount;

  const paragraphList: string[] = [];

  for (let i = 0; i < paragraphCount; i++) {
    /* 將整除剩餘的字數平均分配給前幾個段落，確保總計達到需求 */
    const targetMinLen = baseCountPerParagraph + (i < remainder ? 1 : 0);
    const paragraphText = generateParagraph(data, topic, targetMinLen);
    paragraphList.push(paragraphText);
  }

  return paragraphList;
}
