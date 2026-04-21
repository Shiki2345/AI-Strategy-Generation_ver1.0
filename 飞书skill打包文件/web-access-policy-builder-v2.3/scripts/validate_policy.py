#!/usr/bin/env python3
"""
Web访问策略配置验证脚本
验证生成的策略配置是否符合schema要求
"""

import json
import re
from datetime import datetime
import sys
from typing import Dict, List, Optional, Tuple


class PolicyValidator:
    """策略配置验证器"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def validate(self, config: Dict) -> Tuple[bool, List[str], List[str]]:
        """验证策略配置
        
        Args:
            config: 策略配置字典
            
        Returns:
            (是否有效, 错误列表, 警告列表)
        """
        self.errors = []
        self.warnings = []
        
        # 基础验证
        self._validate_basic_structure(config)
        
        # 策略ID验证
        self._validate_policy_id(config.get('policy_id', ''))
        
        # 时间验证
        self._validate_schedule(config.get('schedule', {}))
        
        # 域名验证
        self._validate_domains(config.get('restrictions', {}))
        
        # 审批流程验证
        self._validate_approval_process(config.get('approval_process', {}))
        
        # 字段完整性验证
        self._validate_completeness(config)
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _validate_basic_structure(self, config: Dict):
        """验证基础结构"""
        required_fields = [
            'policy_id', 'policy_name', 'policy_type', 'description',
            'status', 'created_at', 'created_by'
        ]
        
        for field in required_fields:
            if field not in config:
                self.errors.append(f"缺少必填字段: {field}")
            elif not config[field]:
                self.errors.append(f"字段不能为空: {field}")
        
        # 验证policy_type
        valid_policy_types = ['specific_website', 'global_website']
        policy_type = config.get('policy_type')
        if policy_type and policy_type not in valid_policy_types:
            self.errors.append(f"无效的policy_type: {policy_type}，必须是 {valid_policy_types}")
    
    def _validate_policy_id(self, policy_id: str):
        """验证策略ID格式"""
        if not policy_id:
            self.errors.append("policy_id不能为空")
            return
        
        pattern = r'^WEB_ACCESS_POLICY_\d{3}$'
        if not re.match(pattern, policy_id):
            self.errors.append(f"policy_id格式错误: {policy_id}，必须匹配 {pattern}")
    
    def _validate_schedule(self, schedule: Dict):
        """验证时间安排"""
        if not schedule:
            self.warnings.append("schedule为空，使用默认时间设置")
            return
        
        # 验证时区
        timezone = schedule.get('timezone')
        if timezone and not self._is_valid_timezone(timezone):
            self.errors.append(f"无效的时区: {timezone}")
        
        # 验证时间范围
        time_ranges = schedule.get('time_ranges', [])
        if time_ranges:
            for i, time_range in enumerate(time_ranges):
                if 'start' not in time_range or 'end' not in time_range:
                    self.errors.append(f"时间范围{i+1}缺少start或end字段")
                else:
                    if not self._is_valid_time_format(time_range['start']):
                        self.errors.append(f"无效的开始时间格式: {time_range['start']}")
                    if not self._is_valid_time_format(time_range['end']):
                        self.errors.append(f"无效的结束时间格式: {time_range['end']}")
                    
                    # 检查时间范围有效性
                    if time_range['start'] and time_range['end']:
                        if time_range['start'] >= time_range['end']:
                            self.errors.append(f"时间范围{i+1}: 开始时间必须早于结束时间")
    
    def _validate_domains(self, restrictions: Dict):
        """验证域名"""
        if restrictions.get('type') == 'specific_website':
            websites = restrictions.get('websites', [])
            if not websites:
                self.errors.append("specific_website类型必须包含websites列表")
            else:
                for i, website in enumerate(websites):
                    domain = website.get('domain')
                    if not domain:
                        self.errors.append(f"网站{i+1}缺少domain字段")
                    elif not self._is_valid_domain(domain):
                        self.errors.append(f"无效的域名格式: {domain}")
    
    def _validate_approval_process(self, approval: Dict):
        """验证审批流程"""
        if approval.get('required'):
            approver = approval.get('approver')
            if not approver:
                self.errors.append("需要审批时approver字段不能为空")
            
            valid_approvers = ['ceo', 'direct_manager', 'hr_department', 'it_department']
            if approver and approver not in valid_approvers:
                self.warnings.append(f"非标准审批人: {approver}，标准审批人: {valid_approvers}")
            
            max_duration = approval.get('max_duration_hours')
            if max_duration and (max_duration <= 0 or max_duration > 24):
                self.warnings.append(f"max_duration_hours值异常: {max_duration}小时")
    
    def _validate_completeness(self, config: Dict):
        """验证字段完整性"""
        # 检查target_users
        target_users = config.get('target_users', {})
        if not target_users:
            self.warnings.append("target_users为空，使用默认设置")
        elif 'scope' not in target_users:
            self.errors.append("target_users缺少scope字段")
        
        # 检查enforcement
        enforcement = config.get('enforcement', {})
        if not enforcement:
            self.warnings.append("enforcement为空，使用默认设置")
        elif 'action' not in enforcement:
            self.errors.append("enforcement缺少action字段")
        
        # 检查monitoring
        monitoring = config.get('monitoring', {})
        if not monitoring:
            self.warnings.append("monitoring为空，使用默认设置")
    
    def _is_valid_timezone(self, timezone: str) -> bool:
        """验证时区是否有效"""
        # 简化的时区验证，实际应该使用pytz库
        valid_timezones = [
            'Asia/Shanghai', 'Asia/Beijing', 'Asia/Tokyo',
            'America/New_York', 'America/Los_Angeles',
            'Europe/London', 'Europe/Paris'
        ]
        return timezone in valid_timezones
    
    def _is_valid_time_format(self, time_str: str) -> bool:
        """验证时间格式 HH:MM"""
        pattern = r'^([01]?[0-9]|2[0-3]):([0-5][0-9])$'
        return bool(re.match(pattern, time_str))
    
    def _is_valid_domain(self, domain: str) -> bool:
        """验证域名格式"""
        pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        return bool(re.match(pattern, domain))


def validate_policy_file(file_path: str):
    """验证策略配置文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"错误: 文件不存在: {file_path}")
        return False
    except json.JSONDecodeError as e:
        print(f"错误: JSON解析失败: {e}")
        return False
    
    validator = PolicyValidator()
    is_valid, errors, warnings = validator.validate(config)
    
    print(f"\n验证结果: {'✓ 通过' if is_valid else '✗ 失败'}")
    print(f"文件: {file_path}")
    print(f"策略ID: {config.get('policy_id', '未设置')}")
    print(f"策略名称: {config.get('policy_name', '未设置')}")
    
    if warnings:
        print(f"\n警告 ({len(warnings)}个):")
        for warning in warnings:
            print(f"  ⚠ {warning}")
    
    if errors:
        print(f"\n错误 ({len(errors)}个):")
        for error in errors:
            print(f"  ✗ {error}")
    else:
        print("\n✓ 所有验证通过")
    
    return is_valid


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python validate_policy.py <config_file.json>")
        print("示例: python validate_policy.py policy_config.json")
        sys.exit(1)
    
    file_path = sys.argv[1]
    success = validate_policy_file(file_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()