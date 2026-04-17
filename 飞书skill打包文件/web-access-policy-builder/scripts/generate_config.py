#!/usr/bin/env python3
"""
Web访问策略配置生成脚本
根据对话信息生成标准化的策略配置
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any
import argparse


class PolicyGenerator:
    """策略配置生成器"""
    
    def __init__(self, user_name: str = "系统用户", user_email: str = ""):
        self.user_name = user_name
        self.user_email = user_email
        self.policy_counter = 1
    
    def generate_from_conversation(self, conversation_data: Dict) -> Dict:
        """根据对话数据生成配置
        
        Args:
            conversation_data: 包含对话信息的字典
                {
                    "user_query": "用户原始查询",
                    "responses": ["回答1", "回答2", ...],
                    "policy_type": "specific_website" | "global_website",
                    "target_users": {...},
                    "schedule": {...},
                    "restrictions": {...},
                    "approval_process": {...}
                }
            
        Returns:
            生成的策略配置字典
        """
        # 提取对话信息
        user_query = conversation_data.get('user_query', '')
        policy_type = conversation_data.get('policy_type', 'specific_website')
        
        # 生成基础配置
        config = self._generate_base_config(user_query, policy_type)
        
        # 添加各模块配置
        config.update({
            'target_users': self._generate_target_users(
                conversation_data.get('target_users', {})
            ),
            'schedule': self._generate_schedule(
                conversation_data.get('schedule', {})
            ),
            'restrictions': self._generate_restrictions(
                conversation_data.get('restrictions', {}),
                policy_type
            ),
            'approval_process': self._generate_approval_process(
                conversation_data.get('approval_process', {})
            ),
            'enforcement': self._generate_enforcement(),
            'monitoring': self._generate_monitoring()
        })
        
        return config
    
    def _generate_base_config(self, user_query: str, policy_type: str) -> Dict:
        """生成基础配置"""
        # 从用户查询提取策略名称
        policy_name = self._extract_policy_name(user_query, policy_type)
        
        # 生成策略ID
        policy_id = self._generate_policy_id(policy_type, policy_name)
        
        return {
            'policy_id': policy_id,
            'policy_name': policy_name,
            'policy_type': policy_type,
            'description': self._generate_description(user_query),
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'created_by': f"{self.user_name} ({self.user_email})" if self.user_email else self.user_name
        }
    
    def _generate_target_users(self, user_data: Dict) -> Dict:
        """生成目标用户配置"""
        # 从用户数据提取信息，或使用默认值
        scope = user_data.get('scope', 'all_employees')
        exclusions = user_data.get('exclusions', [])
        
        # 解析用户回答中的排除人群
        if 'user_response' in user_data:
            exclusions = self._parse_exclusions(user_data['user_response'])
        
        return {
            'scope': scope,
            'exclusions': exclusions,
            'includes_contractors': user_data.get('includes_contractors', False),
            'includes_interns': user_data.get('includes_interns', True),
            'includes_remote_employees': user_data.get('includes_remote_employees', True),
            'includes_temporary': user_data.get('includes_temporary', False)
        }
    
    def _generate_schedule(self, schedule_data: Dict) -> Dict:
        """生成时间安排配置"""
        # 默认设置
        default_schedule = {
            'timezone': 'Asia/Shanghai',
            'recurrence': 'weekly',
            'weekdays': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
            'time_ranges': [
                {
                    'start': '09:00',
                    'end': '18:00'
                }
            ],
            'exclude_holidays': True,
            'holiday_schedule': 'national_holidays'
        }
        
        # 如果用户提供了具体时间，使用用户数据
        if schedule_data.get('user_response'):
            parsed_schedule = self._parse_schedule_response(schedule_data['user_response'])
            default_schedule.update(parsed_schedule)
        else:
            # 使用用户提供的数据覆盖默认值
            default_schedule.update(schedule_data)
        
        return default_schedule
    
    def _generate_restrictions(self, restrictions_data: Dict, policy_type: str) -> Dict:
        """生成限制内容配置"""
        if policy_type == 'specific_website':
            return self._generate_specific_website_restrictions(restrictions_data)
        else:  # global_website
            return self._generate_global_website_restrictions(restrictions_data)
    
    def _generate_specific_website_restrictions(self, data: Dict) -> Dict:
        """生成特定网站限制配置"""
        websites = []
        
        # 从用户回答解析网站列表
        if 'user_response' in data:
            websites = self._parse_websites(data['user_response'])
        elif 'websites' in data:
            websites = data['websites']
        else:
            # 默认社交媒体网站列表
            websites = [
                {'domain': 'weibo.com', 'name': '微博', 'block_type': 'complete'},
                {'domain': 'douyin.com', 'name': '抖音网页版', 'block_type': 'complete'},
                {'domain': 'xiaohongshu.com', 'name': '小红书', 'block_type': 'complete'}
            ]
        
        return {
            'type': 'website_blocking',
            'websites': websites,
            'block_level': 'domain_level',
            'exceptions': {
                'allowed_urls': data.get('allowed_urls', []),
                'allowed_ips': data.get('allowed_ips', [])
            }
        }
    
    def _generate_global_website_restrictions(self, data: Dict) -> Dict:
        """生成全局网站限制配置"""
        # 从用户回答解析操作限制
        if 'user_response' in data:
            parsed_ops = self._parse_operations(data['user_response'])
            data.update(parsed_ops)
        
        return {
            'type': 'operation_control',
            'allowed_operations': data.get('allowed_operations', ['browse', 'view']),
            'blocked_operations': data.get('blocked_operations', ['download', 'print', 'upload', 'copy']),
            'file_types': {
                'blocked': data.get('blocked_file_types', ['exe', 'zip', 'rar']),
                'allowed': data.get('allowed_file_types', ['pdf', 'docx', 'xlsx'])
            }
        }
    
    def _generate_approval_process(self, data: Dict) -> Dict:
        """生成审批流程配置"""
        # 从用户回答解析审批信息
        if 'user_response' in data:
            parsed_approval = self._parse_approval_response(data['user_response'])
            data.update(parsed_approval)
        
        required = data.get('required', True)
        
        if required:
            return {
                'required': True,
                'approver': data.get('approver', 'ceo'),
                'method': data.get('method', 'online'),
                'max_duration_hours': data.get('max_duration_hours', 4),
                'requires_reason': data.get('requires_reason', True),
                'auto_revoke_after_hours': data.get('auto_revoke_after_hours', 8),
                'notification_channels': data.get('notification_channels', ['email', 'im']),
                'escalation_policy': data.get('escalation_policy', 'manager_chain')
            }
        else:
            return {
                'required': False,
                'approver': '',
                'method': 'none',
                'max_duration_hours': 0,
                'requires_reason': False,
                'auto_revoke_after_hours': 0
            }
    
    def _generate_enforcement(self) -> Dict:
        """生成执行机制配置"""
        return {
            'action': 'block_with_notification',
            'notification_message': '当前访问受限，根据公司策略需要特殊审批。',
            'redirect_url': None,
            'logging_level': 'detailed',
            'grace_period_minutes': 5,
            'remediation_steps': ['申请特殊权限', '联系IT支持']
        }
    
    def _generate_monitoring(self) -> Dict:
        """生成监控机制配置"""
        return {
            'alert_threshold': 5,
            'report_frequency': 'weekly',
            'notify_admins': ['it_department', 'hr_department', 'security_team'],
            'metrics': ['access_attempts', 'approval_requests', 'violations'],
            'retention_days': 90
        }
    
    # 解析辅助方法
    
    def _extract_policy_name(self, user_query: str, policy_type: str) -> str:
        """从用户查询提取策略名称"""
        # 简单提取关键词
        keywords = {
            '上班时间': '工作时间',
            '社交媒体': '社交媒体',
            '禁止访问': '访问限制',
            '限制': '限制',
            '下载': '下载',
            '打印': '打印',
            '上传': '上传'
        }
        
        name_parts = []
        for keyword, display in keywords.items():
            if keyword in user_query:
                name_parts.append(display)
        
        if not name_parts:
            name_parts = ['网页访问']
        
        if policy_type == 'specific_website':
            policy_type_str = '特定网站'
        else:
            policy_type_str = '全局网站'
        
        return f"{policy_type_str}{''.join(name_parts)}策略"
    
    def _generate_policy_id(self, policy_type: str, policy_name: str) -> str:
        """生成策略ID"""
        # 根据策略类型确定前缀
        if policy_type == 'specific_website':
            type_code = '01'
        else:
            type_code = '02'
        
        # 从策略名称提取简写
        name_code = ''.join([c for c in policy_name if c.isalpha()])[:3].upper()
        if not name_code:
            name_code = 'POL'
        
        # 生成序号
        seq_num = str(self.policy_counter).zfill(3)
        self.policy_counter += 1
        
        return f"WEB_ACCESS_POLICY_{type_code}_{name_code}_{seq_num}"
    
    def _generate_description(self, user_query: str) -> str:
        """生成策略描述"""
        # 简单的描述生成
        if '上班时间' in user_query and '社交媒体' in user_query:
            return "在工作时间限制员工访问社交媒体网站，提高工作效率"
        elif '下载' in user_query:
            return "控制员工文件下载权限，防止数据泄露"
        elif '所有网站' in user_query:
            return "全局网站操作权限控制策略"
        else:
            return "网页访问控制策略"
    
    def _parse_exclusions(self, response: str) -> List[str]:
        """从用户回答解析排除人群"""
        exclusions = []
        
        # 常见模式
        if '除了老板外的所有员工' in response:
            exclusions.append('ceo')
        elif '除管理层外' in response:
            exclusions.append('management')
        elif '高管除外' in response:
            exclusions.append('executives')
        
        return exclusions
    
    def _parse_schedule_response(self, response: str) -> Dict:
        """从用户回答解析时间安排"""
        result = {}
        
        # 解析工作日
        weekdays_map = {
            '周一': 'monday', '周二': 'tuesday', '周三': 'wednesday',
            '周四': 'thursday', '周五': 'friday', '周六': 'saturday', '周日': 'sunday'
        }
        
        weekdays = []
        for chinese, english in weekdays_map.items():
            if chinese in response:
                weekdays.append(english)
        
        if weekdays:
            result['weekdays'] = weekdays
        
        # 解析时间段
        time_pattern = r'(\d{1,2}):?(\d{2})?\s*[到\-]\s*(\d{1,2}):?(\d{2})?'
        match = re.search(time_pattern, response)
        if match:
            start_hour = match.group(1)
            start_min = match.group(2) or '00'
            end_hour = match.group(3)
            end_min = match.group(4) or '00'
            
            result['time_ranges'] = [{
                'start': f"{start_hour.zfill(2)}:{start_min}",
                'end': f"{end_hour.zfill(2)}:{end_min}"
            }]
        
        return result
    
    def _parse_websites(self, response: str) -> List[Dict]:
        """从用户回答解析网站列表"""
        websites = []
        
        # 域名映射
        domain_map = {
            '微博': 'weibo.com',
            '抖音': 'douyin.com',
            '小红书': 'xiaohongshu.com',
            'Facebook': 'facebook.com',
            'Twitter': 'twitter.com',
            'Instagram': 'instagram.com',
            '微信': 'weixin.qq.com',
            '知乎': 'zhihu.com'
        }
        
        # 匹配域名模式
        domain_pattern = r'([a-zA-Z0-9-]+\.(?:com|cn|net|org))'
        domain_matches = re.findall(domain_pattern, response)
        
        for domain in domain_matches:
            websites.append({
                'domain': domain,
                'name': self._get_website_name(domain),
                'block_type': 'complete'
            })
        
        # 匹配中文网站名
        for chinese_name, domain in domain_map.items():
            if chinese_name in response and domain not in [w['domain'] for w in websites]:
                websites.append({
                    'domain': domain,
                    'name': chinese_name,
                    'block_type': 'complete'
                })
        
        return websites
    
    def _parse_operations(self, response: str) -> Dict:
        """从用户回答解析操作限制"""
        result = {
            'allowed_operations': ['browse', 'view'],
            'blocked_operations': []
        }
        
        operations_map = {
            '下载': 'download',
            '打印': 'print',
            '上传': 'upload',
            '复制': 'copy',
            '分享': 'share',
            '保存': 'save'
        }
        
        for chinese, english in operations_map.items():
            if chinese in response:
                result['blocked_operations'].append(english)
        
        return result
    
    def _parse_approval_response(self, response: str) -> Dict:
        """从用户回答解析审批信息"""
        result = {}
        
        # 检查是否需要审批
        if '需要申请' in response or '需要审批' in response:
            result['required'] = True
        elif '不需要' in response or '无需' in response:
            result['required'] = False
            return result
        
        # 解析审批人
        approver_map = {
            'BOSS': 'ceo',
            '老板': 'ceo',
            'CEO': 'ceo',
            '主管': 'direct_manager',
            '直属主管': 'direct_manager',
            '经理': 'direct_manager',
            'HR': 'hr_department',
            '人事': 'hr_department',
            'IT': 'it_department',
            '技术': 'it_department'
        }
        
        for keyword, approver in approver_map.items():
            if keyword in response:
                result['approver'] = approver
                break
        
        # 解析审批方式
        if '线上' in response or '在线' in response:
            result['method'] = 'online'
        elif '线下' in response or '当面' in response:
            result['method'] = 'offline'
        
        return result
    
    def _get_website_name(self, domain: str) -> str:
        """根据域名获取网站名称"""
        name_map = {
            'weibo.com': '微博',
            'douyin.com': '抖音',
            'xiaohongshu.com': '小红书',
            'facebook.com': 'Facebook',
            'twitter.com': 'Twitter',
            'instagram.com': 'Instagram',
            'zhihu.com': '知乎'
        }
        return name_map.get(domain, domain)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='生成Web访问策略配置')
    parser.add_argument('--user-name', default='系统用户', help='用户姓名')
    parser.add_argument('--user-email', default='', help='用户邮箱')
    parser.add_argument('--output', default='policy_config.json', help='输出文件路径')
    parser.add_argument('--example', action='store_true', help='生成示例配置')
    
    args = parser.parse_args()
    
    generator = PolicyGenerator(args.user_name, args.user_email)
    
    if args.example:
        # 生成示例配置
        example_data = {
            'user_query': '我想在上班时间禁止员工访问社交媒体网站',
            'policy_type': 'specific_website',
            'target_users': {
                'user_response': '除了老板外的所有员工',
                'includes_interns': True
            },
            'schedule': {
                'user_response': '周一到周五，早上9点到下午6点（标准工作时间）'
            },
            'restrictions': {
                'user_response': '微博、抖音网页版、小红书、Facebook、Twitter/X、Instagram'
            },
            'approval_process': {
                'user_response': '需要申请特殊权限，由BOSS线上审批'
            }
        }
        
        config = generator.generate_from_conversation(example_data)
    else:
        # 这里可以扩展为从文件读取对话数据
        print("请提供对话数据或使用--example参数生成示例配置")
        return
    
    # 保存配置
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"配置已生成: {args.output}")
    print(f"策略ID: {config['policy_id']}")
    print(f"策略名称: {config['policy_name']}")


if __name__ == "__main__":
    main()