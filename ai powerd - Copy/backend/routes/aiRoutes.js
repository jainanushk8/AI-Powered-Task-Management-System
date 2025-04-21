const express = require('express');
const router = express.Router();
const aiController = require('../aiRoutes/aiController');

router.post('/sentiment', aiController.analyzeSentiment);
router.post('/optimize-task', aiController.optimizeTask);
router.post('/schedule-predict', aiController.scheduleAndPredict);

module.exports = router;
