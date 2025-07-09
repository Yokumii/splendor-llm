#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import argparse
from rich.console import Console

from agents.llm_agent import LLMAgent
from utils.config_loader import load_config, get_model_config
from utils.llm_factory import create_llm_client
from game.action import Action, ActionType

console = Console()

def test_llm_agent(model_name):
    """测试LLM代理能否正常工作"""
    console.print(f"[bold cyan]测试LLM代理: {model_name}[/bold cyan]")
    
    try:
        # 加载配置
        config = load_config()
        model_config = get_model_config(config, model_name)
        
        if not model_config:
            console.print(f"[bold red]错误: 未找到模型 '{model_name}' 的配置[/bold red]")
            return False
        
        # 创建LLM客户端
        console.print(f"[cyan]创建LLM客户端: {model_config.get('type')}[/cyan]")
        llm_client = create_llm_client(model_config)
        
        # 创建LLM代理
        console.print(f"[cyan]创建LLM代理...[/cyan]")
        agent = LLMAgent(
            player_id="test_agent",
            name=f"{model_name} 测试代理",
            llm_client=llm_client,
            temperature=model_config.get("temperature", 0.7)
        )
        
        # 测试简单查询
        console.print("[cyan]测试简单查询...[/cyan]")
        
        # 创建模拟游戏状态
        game_state = {
            "current_player": "test_agent",
            "players": [
                {
                    "id": "test_agent",
                    "name": "测试玩家",
                    "score": 0,
                    "gems": {"red": 2, "blue": 1, "green": 0, "white": 1, "black": 0, "gold": 0},
                    "reserved_cards": [],
                    "purchased_cards": []
                }
            ],
            "board": {
                "tier1_cards": [{"id": "card1", "cost": {"red": 2, "blue": 1}}],
                "tier2_cards": [],
                "tier3_cards": [],
                "nobles": [],
                "gems": {"red": 4, "blue": 4, "green": 4, "white": 4, "black": 4, "gold": 5}
            }
        }
        
        # 创建模拟动作
        valid_actions = [
            Action(action_type=ActionType.TAKE_DIFFERENT_GEMS, params={"colors": ["red", "blue", "green"]}),
            Action(action_type=ActionType.TAKE_SAME_GEMS, params={"color": "red"}),
            Action(action_type=ActionType.BUY_CARD, params={"card_id": "card1"})
        ]
        
        # 测试select_action
        console.print("[cyan]测试select_action方法...[/cyan]")
        action = agent.select_action(game_state, valid_actions)
        
        if action:
            console.print(f"[green]代理选择了动作: {action}[/green]")
            return True
        else:
            console.print(f"[bold red]错误: 代理未能选择动作[/bold red]")
            return False
        
    except Exception as e:
        console.print(f"[bold red]测试过程出错: {e}[/bold red]")
        import traceback
        console.print(f"[red]{traceback.format_exc()}[/red]")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="测试LLM代理")
    parser.add_argument("model", type=str, help="要测试的模型名称")
    
    args = parser.parse_args()
    
    success = test_llm_agent(args.model)
    sys.exit(0 if success else 1) 