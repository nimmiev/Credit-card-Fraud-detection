/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 10.4.25-MariaDB : Database - credit_card_py
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`credit_card_py` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `credit_card_py`;

/*Table structure for table `account` */

DROP TABLE IF EXISTS `account`;

CREATE TABLE `account` (
  `account_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `accountnumber` varchar(100) DEFAULT NULL,
  `balance` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`account_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `account` */

insert  into `account`(`account_id`,`user_id`,`accountnumber`,`balance`,`status`) values 
(1,1,'796837425198','50350','pending'),
(2,4,'908155226890','3150','pending'),
(3,2,'525446101366','5000','pending');

/*Table structure for table `creditcard` */

DROP TABLE IF EXISTS `creditcard`;

CREATE TABLE `creditcard` (
  `creditcard_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `cardnum` varchar(100) DEFAULT NULL,
  `month` varchar(100) DEFAULT NULL,
  `pin_no` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `balance` varchar(100) DEFAULT NULL,
  `ifsc_code` varchar(100) DEFAULT NULL,
  `acc_no` varchar(100) DEFAULT NULL,
  `cvv` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`creditcard_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `creditcard` */

insert  into `creditcard`(`creditcard_id`,`user_id`,`cardnum`,`month`,`pin_no`,`date`,`balance`,`ifsc_code`,`acc_no`,`cvv`,`status`) values 
(1,1,'2032422102422032','2022-01','6585','2022-10-19','51650','65498','987654321012','459','pending'),
(2,2,'6542846593716474','2022-05','6548','2022-10-19','5000','32658','415686988433','987','blocked'),
(4,4,'6876941313540074','2022-09','7654','2022-10-19','3500','32135','120078000467','963','blocked'),
(6,3,'1200151000657483','2022-12','2145','2022-10-20','0','32554','321654987326','765','accept');

/*Table structure for table `detect` */

DROP TABLE IF EXISTS `detect`;

CREATE TABLE `detect` (
  `detect_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `sttaus` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`detect_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4;

/*Data for the table `detect` */

insert  into `detect`(`detect_id`,`user_id`,`sttaus`) values 
(2,2,'pending'),
(3,2,'pending'),
(4,2,'pending'),
(5,2,'pending');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `usertype` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values 
(1,'nimmiev','123456','user'),
(2,'mini','123456','user'),
(3,'elsa','123456','user'),
(4,'fahee','123','user'),
(5,'appu','123','user'),
(6,'admin','admin','admin');

/*Table structure for table `request` */

DROP TABLE IF EXISTS `request`;

CREATE TABLE `request` (
  `request_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `details` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`request_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

/*Data for the table `request` */

insert  into `request`(`request_id`,`user_id`,`details`,`date`,`status`) values 
(1,1,'banking','2022-10-19','accept'),
(2,2,'Ebanking','2022-10-19','accept'),
(3,4,'banking','2022-10-19','accept'),
(5,5,'banking','2022-10-20','reject'),
(6,3,'ebanking','2022-10-20','pending');

/*Table structure for table `transaction` */

DROP TABLE IF EXISTS `transaction`;

CREATE TABLE `transaction` (
  `transaction_id` int(11) NOT NULL AUTO_INCREMENT,
  `faccount` varchar(100) DEFAULT NULL,
  `taccount` varchar(100) DEFAULT NULL,
  `amount` varchar(100) DEFAULT NULL,
  `latitude` varchar(100) DEFAULT NULL,
  `longitude` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`transaction_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `transaction` */

insert  into `transaction`(`transaction_id`,`faccount`,`taccount`,`amount`,`latitude`,`longitude`,`date`,`status`) values 
(1,'796837425198','908155226890','50',NULL,NULL,'2022-10-20','pending'),
(2,'1','','150',NULL,NULL,'2022-10-28','credit'),
(3,'908155226890','796837425198','200','9.387387387387387','76.62982322978122','2022-10-30','debit'),
(4,'908155226890','796837425198','200','9.36936936936937','76.62584326647574','2022-10-30','debit');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `fname` varchar(100) DEFAULT NULL,
  `lname` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`user_id`,`login_id`,`fname`,`lname`,`place`,`phone`,`email`) values 
(1,1,'Nimmi','E V','Paravur','9856423874','nimmiev222@gmail.com'),
(2,2,'Mini','k v','vypin','9785643824','nimmiev222@gmail.com'),
(3,3,'Elsa','saji','karimukal','6589642837','nimmiev222@gmail.com'),
(4,4,'Faheema','fasal','mala','7018654829','akash.edva@gmail.com'),
(5,5,'appu','v','kaloor','7854658910','nimmiev222@gmail.com');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
