default_scope = 'mmyolo'
default_hooks = dict(
    timer=dict(type='IterTimerHook'),
    logger=dict(type='LoggerHook', interval=1),
    param_scheduler=dict(type='ParamSchedulerHook'),
    checkpoint=dict(
        type='CheckpointHook', interval=1, max_keep_ckpts=2, save_last=True),
    sampler_seed=dict(type='DistSamplerSeedHook'),
    visualization=dict(type='mmdet.DetVisualizationHook'))
env_cfg = dict(
    cudnn_benchmark=True,
    mp_cfg=dict(mp_start_method='fork', opencv_num_threads=0),
    dist_cfg=dict(backend='nccl'))
vis_backends = [
    dict(type='LocalVisBackend'),
]
visualizer = dict(
    type='mmdet.DetLocalVisualizer',
    vis_backends=[
        dict(type='LocalVisBackend'),
    ],
    name='visualizer')
log_processor = dict(type='LogProcessor', window_size=50, by_epoch=True)
log_level = 'INFO'
load_from = None
resume = False
backend_args = None
_backend_args = None
tta_model = dict(
    type='mmdet.DetTTAModel',
    tta_cfg=dict(nms=dict(type='nms', iou_threshold=0.65), max_per_img=300))
img_scales = [
    (
        640,
        640,
    ),
    (
        320,
        320,
    ),
    (
        960,
        960,
    ),
]
_multiscale_resize_transforms = [
    dict(
        type='Compose',
        transforms=[
            dict(type='YOLOv5KeepRatioResize', scale=(
                640,
                640,
            )),
            dict(
                type='LetterResize',
                scale=(
                    640,
                    640,
                ),
                allow_scale_up=False,
                pad_val=dict(img=114)),
        ]),
    dict(
        type='Compose',
        transforms=[
            dict(type='YOLOv5KeepRatioResize', scale=(
                320,
                320,
            )),
            dict(
                type='LetterResize',
                scale=(
                    320,
                    320,
                ),
                allow_scale_up=False,
                pad_val=dict(img=114)),
        ]),
    dict(
        type='Compose',
        transforms=[
            dict(type='YOLOv5KeepRatioResize', scale=(
                960,
                960,
            )),
            dict(
                type='LetterResize',
                scale=(
                    960,
                    960,
                ),
                allow_scale_up=False,
                pad_val=dict(img=114)),
        ]),
]
tta_pipeline = [
    dict(type='LoadImageFromFile', backend_args=None),
    dict(
        type='TestTimeAug',
        transforms=[
            [
                dict(
                    type='Compose',
                    transforms=[
                        dict(type='YOLOv5KeepRatioResize', scale=(
                            640,
                            640,
                        )),
                        dict(
                            type='LetterResize',
                            scale=(
                                640,
                                640,
                            ),
                            allow_scale_up=False,
                            pad_val=dict(img=114)),
                    ]),
                dict(
                    type='Compose',
                    transforms=[
                        dict(type='YOLOv5KeepRatioResize', scale=(
                            320,
                            320,
                        )),
                        dict(
                            type='LetterResize',
                            scale=(
                                320,
                                320,
                            ),
                            allow_scale_up=False,
                            pad_val=dict(img=114)),
                    ]),
                dict(
                    type='Compose',
                    transforms=[
                        dict(type='YOLOv5KeepRatioResize', scale=(
                            960,
                            960,
                        )),
                        dict(
                            type='LetterResize',
                            scale=(
                                960,
                                960,
                            ),
                            allow_scale_up=False,
                            pad_val=dict(img=114)),
                    ]),
            ],
            [
                dict(type='mmdet.RandomFlip', prob=1.0),
                dict(type='mmdet.RandomFlip', prob=0.0),
            ],
            [
                dict(type='mmdet.LoadAnnotations', with_bbox=True),
            ],
            [
                dict(
                    type='mmdet.PackDetInputs',
                    meta_keys=(
                        'img_id',
                        'img_path',
                        'ori_shape',
                        'img_shape',
                        'scale_factor',
                        'pad_param',
                        'flip',
                        'flip_direction',
                    )),
            ],
        ]),
]
data_root = '/home/chaki/INSBench/datasets/MoNuSeg'
train_ann_file = 'annotations/train.json'
train_data_prefix = 'train/'
val_ann_file = 'annotations/val.json'
val_data_prefix = 'val/'
test_ann_file = 'annotations/test.json'
test_data_prefix = 'test/'
num_classes = 1
train_batch_size_per_gpu = 2
train_num_workers = 1
persistent_workers = True
base_lr = 0.01
max_epochs = 800
close_mosaic_epochs = 10
model_test_cfg = dict(
    multi_label=True,
    nms_pre=30000,
    score_thr=0.001,
    nms=dict(type='nms', iou_threshold=0.7),
    max_per_img=1000)
img_scale = (
    512,
    512,
)
dataset_type = 'MoNuSegDataset'
val_batch_size_per_gpu = 1
val_num_workers = 1
batch_shapes_cfg = None
deepen_factor = 0.67
widen_factor = 0.75
strides = [
    8,
    16,
    32,
]
last_stage_out_channels = 768
num_det_layers = 3
norm_cfg = dict(type='BN', momentum=0.03, eps=0.001)
affine_scale = 0.9
max_aspect_ratio = 100
tal_topk = 10
tal_alpha = 0.5
tal_beta = 6.0
loss_cls_weight = 0.5
loss_bbox_weight = 7.5
loss_dfl_weight = 0.375
lr_factor = 0.01
weight_decay = 0.0005
save_epoch_intervals = 5
val_interval_stage2 = 1
max_keep_ckpts = 3
model = dict(
    type='YOLODetector',
    data_preprocessor=dict(
        type='YOLOv5DetDataPreprocessor',
        mean=[
            0.0,
            0.0,
            0.0,
        ],
        std=[
            255.0,
            255.0,
            255.0,
        ],
        bgr_to_rgb=True),
    backbone=dict(
        type='YOLOv8CSPDarknet',
        arch='P5',
        last_stage_out_channels=768,
        deepen_factor=0.67,
        widen_factor=0.75,
        norm_cfg=dict(type='BN', momentum=0.03, eps=0.001),
        act_cfg=dict(type='SiLU', inplace=True)),
    neck=dict(
        type='YOLOv8PAFPN',
        deepen_factor=0.67,
        widen_factor=0.75,
        in_channels=[
            256,
            512,
            768,
        ],
        out_channels=[
            256,
            512,
            768,
        ],
        num_csp_blocks=3,
        norm_cfg=dict(type='BN', momentum=0.03, eps=0.001),
        act_cfg=dict(type='SiLU', inplace=True)),
    bbox_head=dict(
        type='YOLOv8Head',
        head_module=dict(
            type='YOLOv8HeadModule',
            num_classes=1,
            in_channels=[
                256,
                512,
                768,
            ],
            widen_factor=0.75,
            reg_max=16,
            norm_cfg=dict(type='BN', momentum=0.03, eps=0.001),
            act_cfg=dict(type='SiLU', inplace=True),
            featmap_strides=[
                8,
                16,
                32,
            ]),
        prior_generator=dict(
            type='mmdet.MlvlPointGenerator', offset=0.5, strides=[
                8,
                16,
                32,
            ]),
        bbox_coder=dict(type='DistancePointBBoxCoder'),
        loss_cls=dict(
            type='mmdet.CrossEntropyLoss',
            use_sigmoid=True,
            reduction='none',
            loss_weight=0.5),
        loss_bbox=dict(
            type='IoULoss',
            iou_mode='ciou',
            bbox_format='xyxy',
            reduction='sum',
            loss_weight=7.5,
            return_iou=False),
        loss_dfl=dict(
            type='mmdet.DistributionFocalLoss',
            reduction='mean',
            loss_weight=0.375)),
    train_cfg=dict(
        assigner=dict(
            type='BatchTaskAlignedAssigner',
            num_classes=1,
            use_ciou=True,
            topk=10,
            alpha=0.5,
            beta=6.0,
            eps=1e-09)),
    test_cfg=dict(
        multi_label=True,
        nms_pre=30000,
        score_thr=0.001,
        nms=dict(type='nms', iou_threshold=0.7),
        max_per_img=1000))
albu_train_transforms = [
    dict(type='Blur', p=0.01),
    dict(type='MedianBlur', p=0.01),
    dict(type='ToGray', p=0.01),
    dict(type='CLAHE', p=0.01),
]
pre_transform = [
    dict(type='LoadImageFromFile', backend_args=None),
    dict(
        type='LoadAnnotations', with_bbox=True, with_mask=True,
        mask2bbox=True),
]
last_transform = [
    dict(type='RemoveDataElement', keys=[
        'gt_masks',
    ]),
    dict(
        type='mmdet.Albu',
        transforms=[
            dict(type='Blur', p=0.01),
            dict(type='MedianBlur', p=0.01),
            dict(type='ToGray', p=0.01),
            dict(type='CLAHE', p=0.01),
        ],
        bbox_params=dict(
            type='BboxParams',
            format='pascal_voc',
            label_fields=[
                'gt_bboxes_labels',
                'gt_ignore_flags',
            ]),
        keymap=dict(img='image', gt_bboxes='bboxes')),
    dict(type='YOLOv5HSVRandomAug'),
    dict(type='mmdet.RandomFlip', prob=0.5),
    dict(
        type='mmdet.PackDetInputs',
        meta_keys=(
            'img_id',
            'img_path',
            'ori_shape',
            'img_shape',
            'flip',
            'flip_direction',
        )),
]
train_pipeline = [
    dict(type='LoadImageFromFile', backend_args=None),
    dict(
        type='LoadAnnotations', with_bbox=True, with_mask=True,
        mask2bbox=True),
    dict(
        type='Mosaic',
        img_scale=(
            512,
            512,
        ),
        pad_val=114.0,
        pre_transform=[
            dict(type='LoadImageFromFile', backend_args=None),
            dict(
                type='LoadAnnotations',
                with_bbox=True,
                with_mask=True,
                mask2bbox=True),
        ]),
    dict(type='YOLOv5CopyPaste', prob=0.1),
    dict(
        type='YOLOv5RandomAffine',
        max_rotate_degree=0.0,
        max_shear_degree=0.0,
        max_aspect_ratio=100.0,
        scaling_ratio_range=(
            0.09999999999999998,
            1.9,
        ),
        border=(
            -256,
            -256,
        ),
        border_val=(
            114,
            114,
            114,
        ),
        min_area_ratio=0.01,
        use_mask_refine=True),
    dict(
        type='YOLOv5MixUp',
        prob=0.1,
        pre_transform=[
            dict(type='LoadImageFromFile', backend_args=None),
            dict(
                type='LoadAnnotations',
                with_bbox=True,
                with_mask=True,
                mask2bbox=True),
            dict(
                type='Mosaic',
                img_scale=(
                    512,
                    512,
                ),
                pad_val=114.0,
                pre_transform=[
                    dict(type='LoadImageFromFile', backend_args=None),
                    dict(
                        type='LoadAnnotations',
                        with_bbox=True,
                        with_mask=True,
                        mask2bbox=True),
                ]),
            dict(type='YOLOv5CopyPaste', prob=0.1),
            dict(
                type='YOLOv5RandomAffine',
                max_rotate_degree=0.0,
                max_shear_degree=0.0,
                max_aspect_ratio=100.0,
                scaling_ratio_range=(
                    0.09999999999999998,
                    1.9,
                ),
                border=(
                    -256,
                    -256,
                ),
                border_val=(
                    114,
                    114,
                    114,
                ),
                min_area_ratio=0.01,
                use_mask_refine=True),
        ]),
    dict(type='RemoveDataElement', keys=[
        'gt_masks',
    ]),
    dict(
        type='mmdet.Albu',
        transforms=[
            dict(type='Blur', p=0.01),
            dict(type='MedianBlur', p=0.01),
            dict(type='ToGray', p=0.01),
            dict(type='CLAHE', p=0.01),
        ],
        bbox_params=dict(
            type='BboxParams',
            format='pascal_voc',
            label_fields=[
                'gt_bboxes_labels',
                'gt_ignore_flags',
            ]),
        keymap=dict(img='image', gt_bboxes='bboxes')),
    dict(type='YOLOv5HSVRandomAug'),
    dict(type='mmdet.RandomFlip', prob=0.5),
    dict(
        type='mmdet.PackDetInputs',
        meta_keys=(
            'img_id',
            'img_path',
            'ori_shape',
            'img_shape',
            'flip',
            'flip_direction',
        )),
]
train_pipeline_stage2 = [
    dict(type='LoadImageFromFile', backend_args=None),
    dict(
        type='LoadAnnotations', with_bbox=True, with_mask=True,
        mask2bbox=True),
    dict(type='YOLOv5KeepRatioResize', scale=(
        512,
        512,
    )),
    dict(
        type='LetterResize',
        scale=(
            512,
            512,
        ),
        allow_scale_up=True,
        pad_val=dict(img=114.0)),
    dict(
        type='YOLOv5RandomAffine',
        max_rotate_degree=0.0,
        max_shear_degree=0.0,
        scaling_ratio_range=(
            0.09999999999999998,
            1.9,
        ),
        max_aspect_ratio=100,
        border_val=(
            114,
            114,
            114,
        ),
        min_area_ratio=0.01,
        use_mask_refine=True),
    dict(type='RemoveDataElement', keys=[
        'gt_masks',
    ]),
    dict(
        type='mmdet.Albu',
        transforms=[
            dict(type='Blur', p=0.01),
            dict(type='MedianBlur', p=0.01),
            dict(type='ToGray', p=0.01),
            dict(type='CLAHE', p=0.01),
        ],
        bbox_params=dict(
            type='BboxParams',
            format='pascal_voc',
            label_fields=[
                'gt_bboxes_labels',
                'gt_ignore_flags',
            ]),
        keymap=dict(img='image', gt_bboxes='bboxes')),
    dict(type='YOLOv5HSVRandomAug'),
    dict(type='mmdet.RandomFlip', prob=0.5),
    dict(
        type='mmdet.PackDetInputs',
        meta_keys=(
            'img_id',
            'img_path',
            'ori_shape',
            'img_shape',
            'flip',
            'flip_direction',
        )),
]
train_dataloader = dict(
    batch_size=2,
    num_workers=1,
    persistent_workers=True,
    pin_memory=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    collate_fn=dict(type='yolov5_collate'),
    dataset=dict(
        type='MoNuSegDataset',
        data_root='/home/chaki/INSBench/datasets/MoNuSeg',
        ann_file='annotations/train.json',
        data_prefix=dict(img='train/'),
        filter_cfg=dict(filter_empty_gt=False, min_size=32),
        pipeline=[
            dict(type='LoadImageFromFile', backend_args=None),
            dict(
                type='LoadAnnotations',
                with_bbox=True,
                with_mask=True,
                mask2bbox=True),
            dict(
                type='Mosaic',
                img_scale=(
                    512,
                    512,
                ),
                pad_val=114.0,
                pre_transform=[
                    dict(type='LoadImageFromFile', backend_args=None),
                    dict(
                        type='LoadAnnotations',
                        with_bbox=True,
                        with_mask=True,
                        mask2bbox=True),
                ]),
            dict(type='YOLOv5CopyPaste', prob=0.1),
            dict(
                type='YOLOv5RandomAffine',
                max_rotate_degree=0.0,
                max_shear_degree=0.0,
                max_aspect_ratio=100.0,
                scaling_ratio_range=(
                    0.09999999999999998,
                    1.9,
                ),
                border=(
                    -256,
                    -256,
                ),
                border_val=(
                    114,
                    114,
                    114,
                ),
                min_area_ratio=0.01,
                use_mask_refine=True),
            dict(
                type='YOLOv5MixUp',
                prob=0.1,
                pre_transform=[
                    dict(type='LoadImageFromFile', backend_args=None),
                    dict(
                        type='LoadAnnotations',
                        with_bbox=True,
                        with_mask=True,
                        mask2bbox=True),
                    dict(
                        type='Mosaic',
                        img_scale=(
                            512,
                            512,
                        ),
                        pad_val=114.0,
                        pre_transform=[
                            dict(type='LoadImageFromFile', backend_args=None),
                            dict(
                                type='LoadAnnotations',
                                with_bbox=True,
                                with_mask=True,
                                mask2bbox=True),
                        ]),
                    dict(type='YOLOv5CopyPaste', prob=0.1),
                    dict(
                        type='YOLOv5RandomAffine',
                        max_rotate_degree=0.0,
                        max_shear_degree=0.0,
                        max_aspect_ratio=100.0,
                        scaling_ratio_range=(
                            0.09999999999999998,
                            1.9,
                        ),
                        border=(
                            -256,
                            -256,
                        ),
                        border_val=(
                            114,
                            114,
                            114,
                        ),
                        min_area_ratio=0.01,
                        use_mask_refine=True),
                ]),
            dict(type='RemoveDataElement', keys=[
                'gt_masks',
            ]),
            dict(
                type='mmdet.Albu',
                transforms=[
                    dict(type='Blur', p=0.01),
                    dict(type='MedianBlur', p=0.01),
                    dict(type='ToGray', p=0.01),
                    dict(type='CLAHE', p=0.01),
                ],
                bbox_params=dict(
                    type='BboxParams',
                    format='pascal_voc',
                    label_fields=[
                        'gt_bboxes_labels',
                        'gt_ignore_flags',
                    ]),
                keymap=dict(img='image', gt_bboxes='bboxes')),
            dict(type='YOLOv5HSVRandomAug'),
            dict(type='mmdet.RandomFlip', prob=0.5),
            dict(
                type='mmdet.PackDetInputs',
                meta_keys=(
                    'img_id',
                    'img_path',
                    'ori_shape',
                    'img_shape',
                    'flip',
                    'flip_direction',
                )),
        ]))
test_pipeline = [
    dict(type='LoadImageFromFile', backend_args=None),
    dict(type='YOLOv5KeepRatioResize', scale=(
        512,
        512,
    )),
    dict(
        type='LetterResize',
        scale=(
            512,
            512,
        ),
        allow_scale_up=False,
        pad_val=dict(img=114)),
    dict(type='LoadAnnotations', with_bbox=True, _scope_='mmdet'),
    dict(
        type='mmdet.PackDetInputs',
        meta_keys=(
            'img_id',
            'img_path',
            'ori_shape',
            'img_shape',
            'scale_factor',
            'pad_param',
        )),
]
val_dataloader = dict(
    batch_size=1,
    num_workers=1,
    persistent_workers=True,
    pin_memory=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type='MoNuSegDataset',
        data_root='/home/chaki/INSBench/datasets/MoNuSeg',
        test_mode=True,
        data_prefix=dict(img='val/'),
        ann_file='annotations/val.json',
        pipeline=[
            dict(type='LoadImageFromFile', backend_args=None),
            dict(type='YOLOv5KeepRatioResize', scale=(
                512,
                512,
            )),
            dict(
                type='LetterResize',
                scale=(
                    512,
                    512,
                ),
                allow_scale_up=False,
                pad_val=dict(img=114)),
            dict(type='LoadAnnotations', with_bbox=True, _scope_='mmdet'),
            dict(
                type='mmdet.PackDetInputs',
                meta_keys=(
                    'img_id',
                    'img_path',
                    'ori_shape',
                    'img_shape',
                    'scale_factor',
                    'pad_param',
                )),
        ],
        batch_shapes_cfg=None))
test_dataloader = dict(
    batch_size=1,
    num_workers=1,
    persistent_workers=True,
    pin_memory=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type='MoNuSegDataset',
        data_root='/home/chaki/INSBench/datasets/MoNuSeg',
        test_mode=True,
        data_prefix=dict(img='test/'),
        ann_file='annotations/test.json',
        pipeline=[
            dict(type='LoadImageFromFile', backend_args=None),
            dict(type='YOLOv5KeepRatioResize', scale=(
                512,
                512,
            )),
            dict(
                type='LetterResize',
                scale=(
                    512,
                    512,
                ),
                allow_scale_up=False,
                pad_val=dict(img=114)),
            dict(type='LoadAnnotations', with_bbox=True, _scope_='mmdet'),
            dict(
                type='mmdet.PackDetInputs',
                meta_keys=(
                    'img_id',
                    'img_path',
                    'ori_shape',
                    'img_shape',
                    'scale_factor',
                    'pad_param',
                )),
        ],
        batch_shapes_cfg=None))
param_scheduler = None
optim_wrapper = dict(
    type='OptimWrapper',
    clip_grad=dict(max_norm=10.0),
    optimizer=dict(
        type='SGD',
        lr=0.01,
        momentum=0.937,
        weight_decay=0.0005,
        nesterov=True,
        batch_size_per_gpu=2),
    constructor='YOLOv5OptimizerConstructor')
custom_hooks = [
    dict(
        type='EMAHook',
        ema_type='ExpMomentumEMA',
        momentum=0.0001,
        update_buffers=True,
        strict_load=False,
        priority=49),
    dict(
        type='mmdet.PipelineSwitchHook',
        switch_epoch=790,
        switch_pipeline=[
            dict(type='LoadImageFromFile', backend_args=None),
            dict(
                type='LoadAnnotations',
                with_bbox=True,
                with_mask=True,
                mask2bbox=True),
            dict(type='YOLOv5KeepRatioResize', scale=(
                512,
                512,
            )),
            dict(
                type='LetterResize',
                scale=(
                    512,
                    512,
                ),
                allow_scale_up=True,
                pad_val=dict(img=114.0)),
            dict(
                type='YOLOv5RandomAffine',
                max_rotate_degree=0.0,
                max_shear_degree=0.0,
                scaling_ratio_range=(
                    0.09999999999999998,
                    1.9,
                ),
                max_aspect_ratio=100,
                border_val=(
                    114,
                    114,
                    114,
                ),
                min_area_ratio=0.01,
                use_mask_refine=True),
            dict(type='RemoveDataElement', keys=[
                'gt_masks',
            ]),
            dict(
                type='mmdet.Albu',
                transforms=[
                    dict(type='Blur', p=0.01),
                    dict(type='MedianBlur', p=0.01),
                    dict(type='ToGray', p=0.01),
                    dict(type='CLAHE', p=0.01),
                ],
                bbox_params=dict(
                    type='BboxParams',
                    format='pascal_voc',
                    label_fields=[
                        'gt_bboxes_labels',
                        'gt_ignore_flags',
                    ]),
                keymap=dict(img='image', gt_bboxes='bboxes')),
            dict(type='YOLOv5HSVRandomAug'),
            dict(type='mmdet.RandomFlip', prob=0.5),
            dict(
                type='mmdet.PackDetInputs',
                meta_keys=(
                    'img_id',
                    'img_path',
                    'ori_shape',
                    'img_shape',
                    'flip',
                    'flip_direction',
                )),
        ]),
]
val_evaluator = dict(
    type='mmdet.CocoMetric',
    proposal_nums=(
        100,
        1,
        10,
    ),
    ann_file='/home/chaki/INSBench/datasets/MoNuSeg/annotations/val.json',
    metric='bbox')
test_evaluator = dict(
    type='mmdet.CocoMetric',
    proposal_nums=(
        100,
        1,
        10,
    ),
    ann_file='/home/chaki/INSBench/datasets/MoNuSeg/annotations/val.json',
    metric='bbox')
train_cfg = dict(
    type='EpochBasedTrainLoop',
    max_epochs=800,
    val_interval=5,
    dynamic_intervals=[
        (
            790,
            1,
        ),
    ])
val_cfg = dict(type='ValLoop')
test_cfg = dict(type='TestLoop')
use_mask2refine = True
min_area_ratio = 0.01
mixup_prob = 0.1
copypaste_prob = 0.1
mosaic_affine_transform = [
    dict(
        type='Mosaic',
        img_scale=(
            512,
            512,
        ),
        pad_val=114.0,
        pre_transform=[
            dict(type='LoadImageFromFile', backend_args=None),
            dict(
                type='LoadAnnotations',
                with_bbox=True,
                with_mask=True,
                mask2bbox=True),
        ]),
    dict(type='YOLOv5CopyPaste', prob=0.1),
    dict(
        type='YOLOv5RandomAffine',
        max_rotate_degree=0.0,
        max_shear_degree=0.0,
        max_aspect_ratio=100.0,
        scaling_ratio_range=(
            0.09999999999999998,
            1.9,
        ),
        border=(
            -256,
            -256,
        ),
        border_val=(
            114,
            114,
            114,
        ),
        min_area_ratio=0.01,
        use_mask_refine=True),
]
work_dir = './work_dirs/MoNuSeg/mmyolov8/2023-09-28-01-27-07/'
randomness = dict(seed=0)
