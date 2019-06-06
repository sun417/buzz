CREATE TABLE `poco` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '用户Id',
  `user_name` varchar(40) NOT NULL DEFAULT '' COMMENT '用户名称',
  `city` varchar(40) NOT NULL DEFAULT '' COMMENT '居住城市',
  `email` varchar(100) NOT NULL DEFAULT '' COMMENT '电子邮件',
  `qq` varchar(11) NOT NULL DEFAULT '' COMMENT 'QQ',
  `phone` varchar(11) NOT NULL DEFAULT '' COMMENT '手机',
  `gender` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT '性别 0未知 1男 2女',
  `age` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '年龄',
  `weixin` varchar(20) NOT NULL DEFAULT '' COMMENT '微信',
  `equip` varchar(255) NOT NULL DEFAULT '' COMMENT '装备',
  `introduce` varchar(255) NOT NULL DEFAULT '' COMMENT '个人介绍',
  `level` varchar(10) NOT NULL DEFAULT '' COMMENT '等级',
  `score` int(11) NOT NULL DEFAULT '0' COMMENT '摄影积分',
  `album_count` int(11) NOT NULL DEFAULT '0' COMMENT '作品数量',
  `fans_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '粉丝人数',
  `follow_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '关注人数',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8