DROP TABLE IF EXISTS `패키지`;
CREATE TABLE `패키지` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `이름` varchar(255) NOT NULL DEFAULT 'PACKAGE_NAME',
  `버전` varchar(255) NOT NULL DEFAULT 'PACKAGE_VERSION',
  `회사_이름` varchar(30) NOT NULL DEFAULT 'PACKAGE_COMPANY',  
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8
/*!50100 PARTITION BY LINEAR HASH (id)
PARTITIONS 16 */;

DROP TABLE IF EXISTS `사용자_패키지`;
CREATE TABLE `사용자_패키지` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `access_code` varchar(30) NOT NULL DEFAULT 'PACKAGE_COMPANY',  
  `패키지` varchar(255) NOT NULL DEFAULT 'PACKAGE_NAME',
  PRIMARY KEY (`id`, `access_code`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8
/*!50100 PARTITION BY LINEAR HASH (id)
PARTITIONS 16 */;

DROP TABLE IF EXISTS `사용자_0.0.1.a`;
CREATE TABLE `사용자_0.0.1.a` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `access_code` varchar(255) NOT NULL,
  `SNS` tinyint(4) NOT NULL DEFAULT '1' COMMENT '1:GUEST 2:FACEBOOK 3:GOOGLE 3: 4:KAKAO',
  `운영체제` varchar(255) NOT NULL,
  `언어` tinyint(4) NOT NULL DEFAULT '1' COMMENT '1:日本語 2:英語 3:韓国語 4:中国語（簡体） 5:中国語（繁体） 6:その他',
  `시간대` smallint(6) NOT NULL DEFAULT '0' COMMENT 'レジスト時の端末に設定されていた UTC を記録する。 例として、 東京 は 9 (+9)、 ロンドン は 0、 カルフォルニアは -8 など。',
  `친구_코드` int(9) NOT NULL,
  `등록_날짜` datetime NOT NULL,
  `마지막_접속_날짜` datetime NOT NULL,
  `삭제_여부` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`,`access_code`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8
/*!50100 PARTITION BY LINEAR HASH (id)
PARTITIONS 16 */;

DROP TABLE IF EXISTS `facebook`;
CREATE TABLE `facebook` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` varchar(255) NOT NULL DEFAULT 'YOUR_APP_ID',
  `client_secret` varchar(30) NOT NULL DEFAULT 'YOUR_APP_SECRET',
  `redirect_uri` varchar(30) NOT NULL DEFAULT 'YOUR_CANVAS_PAGE',
  `code` varchar(30) NOT NULL DEFAULT 'THE_CODE_FROM_ABOVE',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8
/*!50100 PARTITION BY LINEAR HASH (id)
PARTITIONS 16 */;

DROP TABLE IF EXISTS `google_plus`;
CREATE TABLE `google_plus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` varchar(255) NOT NULL DEFAULT 'YOUR_APP_ID',
  `client_secret` varchar(30) NOT NULL DEFAULT 'YOUR_URL',
  `redirect_uri` varchar(30) NOT NULL DEFAULT 'YOUR_APP_SECRET',
  `id_token` varchar(30) NOT NULL DEFAULT 'THE_CODE_FROM_ABOVE',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8
/*!50100 PARTITION BY LINEAR HASH (id)
PARTITIONS 16 */;

DROP TABLE IF EXISTS `friends`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `friends` (
  `friend_cd1` int(11) NOT NULL,
  `friend_cd2` int(11) NOT NULL,
  `twitter_link` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0: ツイッター繋がりの友達ではない 1: ツイッター繋がりの友達である ',
  `facebook_link` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0: フェイスブック繋がりの友達ではない 1: フェイスブック繋がりの友達である ',
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '申請：１ 許可：２ 拒否：３ 禁止：４',
  `insert_date` datetime NOT NULL,
  `update_date` datetime NOT NULL,
  PRIMARY KEY (`friend_cd1`,`friend_cd2`),
  KEY `social_friends_status_index` (`status`) USING BTREE,
  KEY `social_friends_friend_cd2_index` (`friend_cd2`) USING BTREE,
  KEY `friends_stat_friend1` (`status`,`friend_cd1`) USING BTREE,
  KEY `friends_stat_friend2` (`status`,`friend_cd2`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8
/*!50100 PARTITION BY LINEAR HASH (friend_cd1)
PARTITIONS 16 */;
/*!40101 SET character_set_client = @saved_cs_client */;


