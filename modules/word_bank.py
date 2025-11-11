"""
词库模块 - Word Bank Module
负责管理词库、随机抽取词语、组成句子
"""

import random
import json
import os
from typing import List, Dict


class WordBank:
    """词库管理类"""
    
    def __init__(self, data_dir: str = "data"):
        """
        初始化词库
        
        Args:
            data_dir: 词库数据目录
        """
        self.data_dir = data_dir
        self.word_banks = {
            "subjects": [],      # 主语
            "verbs": [],         # 动词
            "objects": [],       # 宾语
            "adjectives": [],    # 形容词
            "adverbs": [],       # 副词
            "places": [],        # 地点
            "times": []          # 时间
        }
        self.load_default_words()
    
    def load_default_words(self):
        """加载默认词库"""
        self.word_banks = {
            "subjects": [
                "a cat", "a dog", "a girl", "a boy", "an artist",
                "a scientist", "a robot", "a dragon", "a fairy", "a wizard"
            ],
            "verbs": [
                "is running", "is jumping", "is dancing", "is flying", "is swimming",
                "is painting", "is singing", "is reading", "is playing", "is sleeping"
            ],
            "objects": [
                "a ball", "a book", "a flower", "a star", "a rainbow",
                "a sword", "a guitar", "a painting", "a castle", "a spaceship"
            ],
            "adjectives": [
                "beautiful", "magical", "colorful", "mysterious", "ancient",
                "glowing", "floating", "sparkling", "peaceful", "energetic"
            ],
            "adverbs": [
                "happily", "slowly", "quickly", "gracefully", "carefully",
                "mysteriously", "peacefully", "energetically", "gently", "wildly"
            ],
            "places": [
                "in the forest", "on the beach", "in the city", "in the mountains", "in space",
                "in a garden", "under the stars", "by the river", "in a castle", "on a cloud"
            ],
            "times": [
                "at sunset", "at dawn", "at midnight", "in the morning", "in the evening",
                "during spring", "in winter", "on a rainy day", "on a sunny day", "under the moonlight"
            ]
        }
    
    def load_from_file(self, filepath: str):
        """
        从JSON文件加载词库
        
        Args:
            filepath: JSON文件路径
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.word_banks.update(data)
            print(f"✅ 词库加载成功: {filepath}")
        except Exception as e:
            print(f"❌ 词库加载失败: {e}")
    
    def save_to_file(self, filepath: str):
        """
        保存词库到JSON文件
        
        Args:
            filepath: JSON文件路径
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.word_banks, f, ensure_ascii=False, indent=2)
            print(f"✅ 词库保存成功: {filepath}")
        except Exception as e:
            print(f"❌ 词库保存失败: {e}")
    
    def add_word(self, category: str, word: str):
        """
        添加单词到词库
        
        Args:
            category: 词性类别
            word: 单词
        """
        if category in self.word_banks:
            if word not in self.word_banks[category]:
                self.word_banks[category].append(word)
                print(f"✅ 已添加 '{word}' 到 {category}")
            else:
                print(f"⚠️ '{word}' 已存在于 {category}")
        else:
            print(f"❌ 未知的类别: {category}")
    
    def remove_word(self, category: str, word: str):
        """
        从词库中删除单词
        
        Args:
            category: 词性类别
            word: 单词
        """
        if category in self.word_banks:
            if word in self.word_banks[category]:
                self.word_banks[category].remove(word)
                print(f"✅ 已删除 '{word}' 从 {category}")
            else:
                print(f"⚠️ '{word}' 不存在于 {category}")
        else:
            print(f"❌ 未知的类别: {category}")
    
    def get_random_word(self, category: str) -> str:
        """
        从指定类别随机获取一个单词
        
        Args:
            category: 词性类别
            
        Returns:
            随机选择的单词
        """
        if category in self.word_banks and self.word_banks[category]:
            return random.choice(self.word_banks[category])
        return ""
    
    def generate_simple_sentence(self) -> Dict[str, str]:
        """
        生成简单句子: 主语 + 动词 + 宾语
        
        Returns:
            包含句子和各部分的字典
        """
        subject = self.get_random_word("subjects")
        verb = self.get_random_word("verbs")
        obj = self.get_random_word("objects")
        
        sentence = f"{subject} {verb} {obj}"
        
        return {
            "sentence": sentence,
            "subject": subject,
            "verb": verb,
            "object": obj,
            "pattern": "Subject + Verb + Object"
        }
    
    def generate_detailed_sentence(self) -> Dict[str, str]:
        """
        生成详细句子: 形容词 + 主语 + 副词 + 动词 + 形容词 + 宾语 + 地点 + 时间
        
        Returns:
            包含句子和各部分的字典
        """
        adj1 = self.get_random_word("adjectives")
        subject = self.get_random_word("subjects")
        adverb = self.get_random_word("adverbs")
        verb = self.get_random_word("verbs")
        adj2 = self.get_random_word("adjectives")
        obj = self.get_random_word("objects")
        place = self.get_random_word("places")
        time = self.get_random_word("times")
        
        sentence = f"{adj1} {subject} {adverb} {verb} {adj2} {obj} {place} {time}"
        
        return {
            "sentence": sentence,
            "adjective1": adj1,
            "subject": subject,
            "adverb": adverb,
            "verb": verb,
            "adjective2": adj2,
            "object": obj,
            "place": place,
            "time": time,
            "pattern": "Adj + Subj + Adv + Verb + Adj + Obj + Place + Time"
        }
    
    def generate_custom_sentence(self, pattern: List[str]) -> Dict[str, str]:
        """
        根据自定义模式生成句子
        
        Args:
            pattern: 词性列表，如 ["subjects", "verbs", "objects"]
            
        Returns:
            包含句子和各部分的字典
        """
        parts = []
        components = {}
        
        for i, category in enumerate(pattern):
            word = self.get_random_word(category)
            parts.append(word)
            components[f"part_{i}_{category}"] = word
        
        sentence = " ".join(parts)
        components["sentence"] = sentence
        components["pattern"] = " + ".join(pattern)
        
        return components
    
    def get_statistics(self) -> Dict[str, int]:
        """
        获取词库统计信息
        
        Returns:
            各类别的单词数量
        """
        stats = {}
        for category, words in self.word_banks.items():
            stats[category] = len(words)
        return stats
    
    def print_statistics(self):
        """打印词库统计信息"""
        print("\n" + "=" * 50)
        print("📊 词库统计信息")
        print("=" * 50)
        stats = self.get_statistics()
        for category, count in stats.items():
            print(f"{category.ljust(15)}: {count} 个单词")
        print("=" * 50 + "\n")


# 使用示例
if __name__ == "__main__":
    # 创建词库实例
    word_bank = WordBank()
    
    # 打印统计信息
    word_bank.print_statistics()
    
    # 生成简单句子
    print("【简单句子示例】")
    for i in range(3):
        result = word_bank.generate_simple_sentence()
        print(f"{i+1}. {result['sentence']}")
        print(f"   模式: {result['pattern']}\n")
    
    # 生成详细句子
    print("\n【详细句子示例】")
    for i in range(3):
        result = word_bank.generate_detailed_sentence()
        print(f"{i+1}. {result['sentence']}")
        print(f"   模式: {result['pattern']}\n")
    
    # 自定义模式
    print("\n【自定义模式示例】")
    custom_pattern = ["subjects", "verbs", "places", "times"]
    result = word_bank.generate_custom_sentence(custom_pattern)
    print(f"句子: {result['sentence']}")
    print(f"模式: {result['pattern']}")
