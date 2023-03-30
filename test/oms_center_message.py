import re
import time
import requests
import random
import json
import pymysql

from hashlib import md5

file_info_list = []

'''
需要见一个临时表，新创建的翻译资源会写入这个临时表
CREATE TABLE scm_global.vito_temp_sys_message_resource (
  ID bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `KEY` varchar(50) DEFAULT NULL,
  GROUP_NAME varchar(50) NOT NULL,
  SEQUENCE_NUMBER bigint(20) NOT NULL,
  VIEW_TEXT_CH varchar(2000) NOT NULL,
  VIEW_TEXT_EN varchar(2000) NOT NULL,
  FILE_PATH varchar(500) DEFAULT NULL,
  PRIMARY KEY (ID)
)
ENGINE = INNODB,
AUTO_INCREMENT = 24768,
AVG_ROW_LENGTH = 138,
CHARACTER SET utf8,
COLLATE utf8_general_ci;
'''

# 匹配message的正则
# message_regex = r'B.R\("(.*?)"([ ]{0,1},[ ]{0,1}"(.*?)"){0,1}\)'
message_regex = r'"(.*?)"'
zh_message_regex = r'[\u4e00-\u9fa5]+'
# 临时表名称
temp_sys_message_resource_table_name = 'vito_temp_sys_message_resource'
temp_sys_message_resource_table_exists = False

# 数据库连接信息
mysql_connect = {
    "host": '192.168.100.212',
    "port": 3306,
    "user": 'root',
    "passwd": 'tiger_scm',
    "db": 'scm_global'
}

# 需要处理资源文件的cs文件
file_list = [r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Card\CancelConfirmCardNumber.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Card\CancelReverseCardNumber.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Card\ConfirmCardNumber.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Card\CreateOrderByCard.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Card\CreateTransferOrderByCard.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Card\DeleteCardNumber.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Card\DeleteCardNumberDetail.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Card\Import\ImportCardNumber.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Card\ReverseCardNumber.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Card\ReverseOrderByCard.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Card\SaveCardNumber.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Common\ClassExtUtils.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Common\CommonConditionFactory.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Common\CommonMethod.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Common\EnumExt.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Common\LockUtils.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Common\OrderStatusManager.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Common\PackageCommonMethod.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Common\RequestWmsApi.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Common\SaleOrderCheckMethod.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\CreditManage\DeleteCreditLine.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\CBD\CBD_ReleaseSaleOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\CJB\CJB_CreatePurchaseReturnOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\CJB\CJB_UpdatePurchaseOrderUdf.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\CMST\BatchSaveCardNumber.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\DML\SaveErpTransportInventory.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\DML\SavePurchaseDetailTransportInventory.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\Gdcy\PurchaseOrder\GdcyClosePurchaseOrderBeforeCheck.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\Gdcy\PurchaseOrder\GdcyForceClosePurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\Gdcy\PurchaseOrderApplyChange\GdcyGetPurchaseOrderDetailListForChange.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\Gdcy\PurchaseOrderApplyChange\Gdcy_AuditBatchPurchaseOrderApplyChange.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\Gdcy\PurchaseOrderApplyChange\Gdcy_AuditPurchaseOrderApplyChange.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\Gdcy\PurchaseOrderApplyChange\Gdcy_DeletePurchaseOrderApplyChange.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\Gdcy\PurchaseOrderApplyChange\Gdcy_RejectedPurchaseOrderApplyChange.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\Gdcy\PurchaseOrderApplyChange\Gdcy_SaveBatchPurchaseOrderApplyChange.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\Gdcy\PurchaseOrderApplyChange\Gdcy_SavePurchaseOrderApplyChange.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\Gdcy\PurchaseOrderApplyChange\Gdcy_UnAuditPurchaseOrderApplyChange.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\Gdcy\PurchaseOrderApplyChange\PurchaseOrderApplyChangeCommon.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\HXBGY\HXBGYCancelPurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\Kelun\Kelun_ReleasePurchaseDetailList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\BatchUpdatePurchaseFinancialInventoryMarkLP.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\BatchUpdateSaleExternalOrderIdLP.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\BatchUpdateSaleFinancialInventoryMarkLP.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\DSL\LPDSLGetPurchaseOrderFeedbackList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\DSL\LPDSLGetSaleOrderFeedbackList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\DSL\LPDSLSaveSaleOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\EdringtonInsertPurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\EdringtonInsertSaleOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\ImportPurchaseSplitDetailLP.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\ImportUpdateAttrPurchaseDetailLP.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\LPFeedbackOrderBiz.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\MH\LPGetInvTransferFeedbackList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\MH\LPGetPurchaseOrderFeedbackList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\MH\LPGetSaleOrderFeedbackEoDPList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\MH\LPGetSaleOrderFeedbackList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\MHInsertPurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\MHInsertSaleOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\ReleasePurchaseOrderByContainerLP.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\TWEInsertPurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\TWEInsertSaleOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\LIGHTPOINT\WGS\LPWGSSaveSaleOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\METRO\GiftOrder\CancelGiftPurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\METRO\GiftOrder\ImportGiftOrderDetail.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\METRO\GiftOrder\ReleaseGiftOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\METRO\Import\ImportMetroS010PurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\METRO\Import\ImportMetroS011SaleOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\METRO\Import\InnerImportPurchaseOrderByS011.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\METRO\Import\InnerImportSaleOrderByS010.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\METRO\PurchaseContainers\CancelReleasePurchaseContainer.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\METRO\PurchaseContainers\DeletePurchaseContainer.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\METRO\PurchaseContainers\ExportPurchaseContainerDetail.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\METRO\PurchaseContainers\ImportPurchaseContainerDetail.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\METRO\PurchaseContainers\ReleasePurchaseContainer.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\METRO\PurchaseContainers\SavePurchaseContainer.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\MLILY\MlilyClosePurchaseOrderDetailBatch.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\MLILY\MlilyCloseSaleOrderDetailBatch.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\MLILY\MlilyCreatePurchaseOrderWithDetailBatch.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\MLILY\MlilyCreateSaleOrderWithDetailBatch.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\MLILY\MlilyPurchaseOrderBiz.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\MLILY\MlilySaleOrderBiz.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\MLILY\MlilySavePurchaseOrderWithDetailBatch.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\MLILY\MlilySavePurchaseOrderWithDetailChangeBatch.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\MLILY\MlilySaveSaleOrderWithDetailBatch.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\MLILY\MlilySaveSaleOrderWithDetailChangeBatch.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\MLILY\MlilyUpdatePurchaseDetailReceivedQty.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\ROCHE\SaleOrderWarehouseAssign.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\TAK\SchaefflerInsertPurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\AutoAcceptEmergencyOrderForBOH.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\BatchSaveSaleChargeDetail.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\CancelConfirmSaleOrderPartial.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\Erp\BatchClosePurchaseOrderForErp.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\Erp\ClosePurchaseOrderDetailForErp.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\Erp\DeletePurchaseOrderDetailByErpForRZ.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\Erp\DeleteRecieptOrderRestorePurDetailByErpForRZ.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\Erp\ErpSaleOrderCreditQuotaBiz.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\Erp\InnerSplitPurchaseDetailReceiptForErp.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\Erp\SavePurchaseOrderWithDetailForErp.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\Erp\SavePurchaseOrderWithDetailForErpBatch.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\Erp\SplitPurchaseOrderByErp.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\Erp\UpdatePurchaseDetailQtyByErp.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\Erp\UpdateSaleOrderUdf.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\ForceReleaseSaleOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\ForceReleaseSaleOrderV1.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\OnLine\CancelSubmitOnLineSale.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\OnLine\DeleteOnLineSale.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\OnLine\GetOnLineSaleEntity.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\OnLine\SaveOnLineSale.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\OnLine\SaveOnLineSaleDetail.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\OnLine\SubmitOnLineSale.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\SaveOrderSkuCloseList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WINNEX\UpdateSaleOrderTempDisplay.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WSWL\ImportVendorPurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WSWL\ImportWswlPlatformSaleOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WSWL\ImportWswlTransportSaleOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WSWL\WSWLPurchaseOrderProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\WSWL\WswlSaleOrderProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\YNJT\CommonBiz.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\Yuanhua\YhSaleOrderWarehouseAssignStrategy.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Customize\ZoomLion\ReleaseSaleOrderBySkuZone.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\ItemLabelPrintBiz\DefaultImportItemLabelPrintProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\ItemLabelPrintBiz\GDCYImportItemLabelPrintProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\ItemLabelPrintBiz\ZoomlionImportItemLabelPrintProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\PurchaseOrderBiz\CarrefourPurchaseOrderProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\PurchaseOrderBiz\DefaultPurchaseOrderProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\PurchaseOrderBiz\DmlPurchaseOrderProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\PurchaseOrderBiz\LPPurchaseOrderProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\PurchaseOrderBiz\MetroPurchaseOrderProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\PurchaseOrderBiz\PurchaseCommon.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\PurchaseOrderBiz\TCarrefourPurchaseOrderProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\PurchaseOrderBiz\WinnexPurchaseOrderProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\SaleOrderBiz\CarrefourSaleOrderProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\SaleOrderBiz\DefaultSaleOrderMergeProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\SaleOrderBiz\DefaultSaleOrderProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\SaleOrderBiz\LPSaleOrderProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\SaleOrderBiz\SaleOrderCommon.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\SaleOrderBiz\TCarrefourSaleOrderProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\SaleOrderBiz\WinnexSaleOrderProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\SaleOrderBiz\WSWLSaleOrderProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\SaleOrderBiz\YuanhuaSaleOrderProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Factory\SaleOrderImportBiz\WinnexSaleOrderImportProcessor.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\ItemLabelPrint\GetItemLabelPrintDetailList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\ItemLabelPrint\GetItemLabelPrintList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\ItemLabelPrint\GetItemLabelPrintRecordList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\ItemLabelPrint\Import\ImportItemLabelPrint.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Print\PrintItemLabelPrint.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Print\PrintItemLabelPrintDetail.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Print\PrintOrderCenter.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\ProjectManage\CloseProject.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\ProjectManage\DeleteProject.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\ProjectManage\DeleteProjectItem.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\ProjectManage\DeleteProjectScope.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\ProjectManage\Import\ImportProjectManage.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\ProjectManage\SaveProjectDateList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\AdjustPurchaseDetailReceipt.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\BatchClosePurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\BatchClosePurchaseOrderRecover.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\BatchModifyPurchaseOrderWarehouse.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\CancelClickOncePurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\CancelClickOncePurchaseOrderByExtOrderId.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\CancelConfirmPurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\CancelPurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\CancelPurchaseOrderByExternalOrderId.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\CancelReleasePurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\CancelSplitPurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\CancelSplitPurchaseOrderAll.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\CancelSplitPurchaseOrderBatch.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\CheckShelfLifePurchaseChildList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\CheckShelfLifePurchaseOrderList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\ClosePurchaseOrderDetail.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\ClosePurchaseOrderDetailRecover.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\Common\BizFunction.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\ConfirmPurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\CopyPurchase.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\DeletePurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\DeletePurchaseOrderByExternalOrderId.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\ExternalAuditPurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\GetPurchaseOrderListByDataInsulate.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\Import\ImportPurchase.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\Import\ImportPurchaseDetail.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\RejectReleasePurchaseSubDetails.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\ReleasePurchaseDetailList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\ReleasePurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\ReleasePurchaseOrderByOriginalLine.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\ReleasePurchaseOrderDetailLine.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\ReleasePurchaseOrderSubDetail.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\RevokeCancelPurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\RevokeReleasePurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\SavePurchaseDetailUpdateList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\SavePurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\SavePurchaseOrderWithDetailBatch.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\SplitPurchaseDetailList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\SplitPurchaseDetailReceipt.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\SplitPurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\Taison\TaiSonSavePurchaseOrderWithDetail.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\Taison\TaisonSavePurchaseSalesOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\UpdatePurchaseDetailPriceBatch.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\PurchaseOrder\VendorConfirmPurchaseOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleForecast\ImportSaleForecast.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\AssignSaleOrderCarrier.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\AssignSaleOrderWarehouse.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\BatchModifySaleOrderWarehouse.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\CancelAssignSaleOrderCarrier.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\CancelAssignSaleOrderWarehouse.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\CancelClickOnceSaleOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\CancelClickOnceSaleOrderByExtOrderId.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\CancelSaleOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\CancelSaleOrderByExternalOrderId.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\CancelSplitSaleOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\CancelSubmitSaleOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\Common\BizFunction.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\ConfirmSaleOrderDetail.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\CopySaleOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\DeleteSaleOrderByExternalOrderId.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\GetSaleOrderDetailList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\GetSaleOrderListByDataInsulate.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\GetSaleOrderListForSplit.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\Import\ImportSaleOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\Import\ImportSaleOrderDetail.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\Import\ImportSaleOrderPrice.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\QueryBatch\CloseSaleOrderByOrderList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\QueryBatch\CloseSaleOrderByOrderListRecover.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\QueryBatch\GetOrderSkuListForAddOriginalDetail.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\QueryBatch\SaveOrderSkuAlternativeList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\QueryBatch\SaveOrderSkuCloseListRecover.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\QueryBatch\SaveOrderSkuQtyBatchList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\QueryBatch\SaveSaleOrderDateList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\QueryBatch\StraightAddSaleDetailsToWms.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\ReleaseSaleOrderDetail.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\RevokeCancelSaleOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\RevokeReleaseSaleOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\SaleOrderSplit.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\SaveSaleOrderDetailUpdateList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\SaveSaleOrderWithDetailBatch.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\SplitSaleOrderDetailList.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\UpdateSaleOrderDetailReason.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\SaleOrder\UpdateSaleOrderSubRouteId.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\Services\GlobalInventory\GlobalInventoryService.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\VasOrder\CancelConfirmVasOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\VasOrder\CancelSubmitVasOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\VasOrder\ConfirmVasOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\VasOrder\DeleteVasOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\VasOrder\DeleteVasOrderChargeDetail.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\VasOrder\DeleteVasOrderDetail.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\VasOrder\Import\ImportVasOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\VasOrder\SaveVasOrder.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\VasOrder\SaveVasOrderDetail.cs',
    r'D:\quantum-scm\SCM\Service\SCM.OMS.OrderCenter\SCM.OMSOrderCenter.Service\VasOrder\SubmitVasOrder.cs'
]


def create_temp_sys_message_resource_table(database_connect):
    sql = "CREATE TABLE IF NOT EXISTS scm_global.%s (\
                ID bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',\
                `KEY` varchar(50) DEFAULT NULL,\
                GROUP_NAME varchar(50) NOT NULL,\
                SEQUENCE_NUMBER bigint(20) NOT NULL,\
                VIEW_TEXT_CH varchar(2000) NOT NULL,\
                VIEW_TEXT_EN varchar(2000) NOT NULL,\
                FILE_PATH varchar(500) DEFAULT NULL,\
                PRIMARY KEY (ID)\
            )\
            ENGINE = INNODB,\
            AUTO_INCREMENT = 24768,\
            AVG_ROW_LENGTH = 138,\
            CHARACTER SET utf8,\
            COLLATE utf8_general_ci;" % temp_sys_message_resource_table_name

    database_connect.cursor().execute(sql)

    temp_sys_message_resource_table_exists = True


def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def translate_message(message):
    time.sleep(2)

    appid = '20230329001619824'
    appkey = 'DrUuH1mrCrXcpXrLkG4H'
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + message + str(salt) + appkey)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'appid': appid,
        'q': message,
        'from': 'zh',
        'to': 'en',
        'salt': salt,
        'sign': sign
    }

    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    response = requests.post(url, params=payload, headers=headers).json()

    if response and 'trans_result' in response and 'dst' in response['trans_result'][0]:
        return response['trans_result'][0]['dst']
    else:
        return None


def get_message_info_list(file_path):
    group_name = build_group_name(file_path)
    message_list = []

    with open(file_path, encoding='utf-8', mode='r') as file:
        line_index = 0
        while True:
            line_index = line_index + 1
            line = file.readline()
            if not line:
                break

            match = re.compile(message_regex).findall(line)
            if match and len(match) > 0:
                for m in match:
                    m_match = re.compile(zh_message_regex).search(m)
                    if m_match:
                        message_list.append(
                            {
                                "group_name": group_name,
                                "message": m,
                                "line": line_index,
                                "file_path": file_path
                            })
                '''
                for m in match:
                    if m[0] and m[0] != '':
                        message_list.append({
                            "group_name": group_name,
                            "message": m[0],
                            "line": line_index,
                            "file_path": file_path
                        })
                '''
    return message_list


def build_group_name(file_path):
    path_list = file_path.split('SCM.OMSOrderCenter.Service')
    path_list = path_list[len(path_list) - 1].split('\\', )
    path_list = [x for x in path_list if x][0]
    return 'Center_' + path_list


def build_message_param(message_list):
    message_array = ["'%s'" % x for x in message_list]
    message_param = ','.join(message_array)
    return message_param


def search_message_resource(message_list, database_connect):
    result = []
    sql_param = build_message_param(message_list)
    # sql = "SELECT RESOURCE_KEY FROM sys_message_resource WHERE VIEW_TEXT LIKE \'%" + message + "%\' OR RESOURCE_KEY LIKE \'%" + message + "%\'"
    sql = 'SELECT RESOURCE_KEY, VIEW_TEXT FROM sys_message_resource WHERE VIEW_TEXT IN (%s) OR RESOURCE_KEY IN (%s)' % (sql_param, sql_param)
    print(sql)
    print('------------------------------------------------')

    database_cursor = database_connect.cursor()
    database_cursor.execute(sql)
    database_result = database_cursor.fetchall()

    if len(database_result) <= 0:
        return result

    for row in database_result:
        result.append({
            "key": row[0],
            "text_ch": row[1]
        })

    return result


def search_temp_message_resource(message_list, database_connect):
    result = []
    sql_param = build_message_param(message_list)

    if temp_sys_message_resource_table_exists is False:
        create_temp_sys_message_resource_table(database_connect)

    sql = 'SELECT GROUP_NAME, SEQUENCE_NUMBER, `KEY`, VIEW_TEXT_CH, VIEW_TEXT_EN FROM vito_temp_sys_message_resource WHERE VIEW_TEXT_CH IN (%s)' % sql_param
    print(sql)
    print('------------------------------------------------')

    database_cursor = database_connect.cursor()
    database_cursor.execute(sql)
    database_result = database_cursor.fetchall()

    if len(database_result) <= 0:
        return result

    for row in database_result:
        result.append({
            "key": row[2],
            "text_ch": row[3],
            "text_en": row[4]
        })

    return result


def insert_temp_message_resource(message_info, translate_message, database_connect):
    group_name = message_info['group_name']
    message = message_info['message']
    file_path = message_info['file_path']

    if temp_sys_message_resource_table_exists is False:
        create_temp_sys_message_resource_table(database_connect)

    search_sql = r"SELECT (CASE WHEN MAX(SEQUENCE_NUMBER) IS NULL THEN 0 ELSE MAX(SEQUENCE_NUMBER) END) AS SEQUENCE_NUMBER FROM vito_temp_sys_message_resource WHERE GROUP_NAME = '%s' ORDER BY SEQUENCE_NUMBER DESC" % group_name
    print(search_sql)
    print('------------------------------------------------')

    database_cursor = database_connect.cursor()
    database_cursor.execute(search_sql)
    database_result = database_cursor.fetchall()
    sequence_number = int(database_result[0][0]) + 1
    key = '%s_%s' % (group_name, str(int(sequence_number)).zfill(6))

    insert_sql = "INSERT vito_temp_sys_message_resource (GROUP_NAME, SEQUENCE_NUMBER, VIEW_TEXT_CH, VIEW_TEXT_EN, FILE_PATH, `KEY`) "
    insert_sql += "SELECT '%s', %s, '%s','%s','%s','%s' FROM DUAL " % (group_name, sequence_number, message, translate_message.replace("\'", "''"), file_path.replace("\\", "\\\\"), key)
    insert_sql += "WHERE NOT EXISTS(SELECT 1 FROM vito_temp_sys_message_resource WHERE VIEW_TEXT_CH = '%s')" % message
    print(insert_sql)
    print('------------------------------------------------')

    rowcount = database_cursor.execute(insert_sql)
    database_connect.commit()

    if rowcount > 0:
        return {
            "key": key,
            "text_ch": message,
            "text_en": translate_message
        }
    return None


def filter_key(message, resource_list):
    key_list = list(filter(lambda x: x["text_ch"] == message, resource_list))
    if key_list and len(key_list) > 0:
        return key_list[0]
    return None


def build_message_sql(new_key_list):
    result = []
    for info in new_key_list:
        for message in info["message"]:
            result.append("CALL T_MSG('%s','%s','%s');" % (info["key"], message["text"], message["type"]))
    return result


def insert_file_message(file_path):
    database_connect = pymysql.connect(host=mysql_connect["host"], user=mysql_connect["user"], passwd=mysql_connect["passwd"], port=mysql_connect["port"], db=mysql_connect['db'])

    file_message_info_list = []
    message_info_list = get_message_info_list(file_path)
    new_key_list = []

    if len(message_info_list) > 0:
        message_list = [x['message'] for x in message_info_list]
        message_key_list = search_message_resource(message_list, database_connect)
        temp_message_key_list = search_temp_message_resource(message_list, database_connect)

        for message_info in message_info_list:
            message = message_info['message']
            exists_key = filter_key(message, message_key_list)
            new_key = filter_key(message, temp_message_key_list)

            if exists_key is None and new_key is None:
                message_en = translate_message(message)
                new_key = insert_temp_message_resource(message_info, message_en, database_connect)

            if new_key:
                new_key_list.append({
                        "key": new_key['key'],
                        "message": [
                            {"text": new_key["text_ch"], "type": 'zh_cn'},
                            {"text": new_key["text_en"], "type": 'en_us'}
                        ]
                    })

            file_message_info_list.append({
                "message": message,
                "line": message_info["line"],
                "exists_key": exists_key["key"] if exists_key and exists_key.get("key") else None,
                "new_key": new_key["key"] if new_key and new_key.get("key") else None
            })
        database_connect.close()

    return {
        "file_path": file_path,
        "message_info_list": file_message_info_list,
        "new_message_key_sql": build_message_sql(new_key_list)
    }


file_info_list = []
file_length = len(file_list)
file_count = 0

for file_path in file_list:
    file_count = file_count + 1
    print("\n")
    print(str(file_length) + "|" + str(file_count))
    print(file_path)
    print('************************************************')

    file_message_info = insert_file_message(file_path)
    file_info_list.append(file_message_info)

    with open(r"E:\Download\message.json", "w", encoding="utf-8") as file:
        json.dump(file_info_list, file, indent=4, ensure_ascii=False)

    print("\n")
