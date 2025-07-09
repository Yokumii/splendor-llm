#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback
from rich.console import Console
from utils.config_loader import load_config, get_model_config
from utils.llm_factory import create_llm_client

console = Console()

def test_model_connection(model_name):
    """测试特定模型的连接"""
    console.print(f"[cyan]测试模型 '{model_name}' 的连接...[/cyan]")
    
    try:
        # 加载配置
        config = load_config()
        model_config = get_model_config(config, model_name)
        
        if not model_config:
            console.print(f"[bold red]错误: 未找到模型 '{model_name}' 的配置[/bold red]")
            return False
        
        # 检查API密钥
        api_key = model_config.get("api_key")
        if not api_key:
            console.print(f"[bold red]错误: 模型 '{model_name}' 没有API密钥配置[/bold red]")
            return False
        
        # 创建客户端
        console.print(f"[cyan]创建LLM客户端: {model_config.get('type')}[/cyan]")
        llm_client = create_llm_client(model_config)
        
        # 测试简单生成
        console.print("[cyan]测试简单提问...[/cyan]")
        response = llm_client.get_completion(
            system_prompt="你是一个乐于助人的AI助手。",
            user_prompt="你好！"
        )
        
        if not response or len(response.strip()) == 0:
            console.print(f"[bold red]错误: 模型返回空响应[/bold red]")
            return False
            
        console.print(f"[green]模型响应: {response[:100]}...[/green]")
        console.print(f"[bold green]模型 '{model_name}' 连接测试成功！[/bold green]")
        return True
        
    except Exception as e:
        console.print(f"[bold red]测试失败: {e}[/bold red]")
        console.print(f"[red]{traceback.format_exc()}[/red]")
        return False

def test_all_models():
    """测试所有配置的模型"""
    console.print("[bold cyan]===== 模型连接测试 =====[/bold cyan]")
    
    try:
        config = load_config()
        models = config.get("models", [])
        
        if not models:
            console.print("[yellow]配置文件中未找到模型[/yellow]")
            return False
        
        results = []
        for model in models:
            model_name = model.get("name")
            success = test_model_connection(model_name)
            results.append((model_name, success))
            console.print("")  # 添加空行分隔
            
        # 显示总结
        console.print("[bold cyan]===== 测试结果摘要 =====[/bold cyan]")
        all_success = True
        for model_name, success in results:
            status = "[green]通过[/green]" if success else "[red]失败[/red]"
            console.print(f"{model_name}: {status}")
            if not success:
                all_success = False
                
        return all_success
            
    except Exception as e:
        console.print(f"[bold red]测试过程出错: {e}[/bold red]")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 测试特定模型
        success = test_model_connection(sys.argv[1])
        sys.exit(0 if success else 1)
    else:
        # 测试所有模型
        success = test_all_models()
        sys.exit(0 if success else 1) 