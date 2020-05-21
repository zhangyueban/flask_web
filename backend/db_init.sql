-- ----------------------------
-- Table structure for admins
-- ----------------------------
DROP TABLE IF EXISTS "admins";
CREATE TABLE "admins" (
  "id" INTEGER NOT NULL,
  "name" VARCHAR(32),
  "password" VARCHAR(128),
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of admins
-- ----------------------------
INSERT INTO "admins" VALUES (8, 'admin', '$5$rounds=535000$9WoOVzcj7Fvi3FsJ$EnhMCR6iPrgkp3G1iulbz5dAw9apErh2UrbyVD6JQP7');

-- ----------------------------
-- Indexes structure for table admins
-- ----------------------------
CREATE INDEX "ix_admins_name"
ON "admins" (
  "name" ASC
);

-- ----------------------------
-- Table structure for joininfos
-- ----------------------------
DROP TABLE IF EXISTS "joininfos";
CREATE TABLE "joininfos" (
  "id" INTEGER NOT NULL,
  "name" VARCHAR(64),
  "phone" VARCHAR(30),
  "profess" VARCHAR(64),
  "grade" VARCHAR(64),
  "email" VARCHAR(120),
  "group" VARCHAR(64),
  "power" TEXT(2000),
  "pub_date" DATETIME,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of joininfos
-- ----------------------------
INSERT INTO "joininfos" VALUES (1, '李四', 13988888888, '计算机学院', '大一', '123@qq.com', '前端,办公', '测试', '2018-02-10 15:17:05.359195');
INSERT INTO "joininfos" VALUES (2, '王二麻子', 13901019893, '管理学院', '大二', '1248643@qq.com', '视觉,办公', '测试', '2018-02-10 15:19:30.822066');
INSERT INTO "joininfos" VALUES (3, '张如花', 13466666339, '艺术学院', '大一', '1248643@qq.com', '视觉,视频', '测试', '2018-02-10 15:20:35.658574');
INSERT INTO "joininfos" VALUES (5, '杨芳', 13439444944, '计算机学院', '大二', '269875215@qq.com', '后端,前端', '测试', '2018-02-10 15:24:35.316247');
INSERT INTO "joininfos" VALUES (6, '折蓉蓉', 13466777707, '数学学院', '大一', '266455@qq.com', '移动,运营', '测试', '2018-02-10 16:48:40.702816');

-- ----------------------------
-- Indexes structure for table joininfos
-- ----------------------------
CREATE INDEX "ix_joininfos_email"
ON "joininfos" (
  "email" ASC
);
CREATE INDEX "ix_joininfos_name"
ON "joininfos" (
  "name" ASC
);
