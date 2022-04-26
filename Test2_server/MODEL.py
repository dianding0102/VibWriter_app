from __future__ import division
import keras

from keras.layers import Flatten,BatchNormalization

from keras.layers.advanced_activations import LeakyReLU
from keras.layers.convolutional import UpSampling2D, Conv2D
from keras.layers.merge import add
from keras.models import Sequential

from keras.layers import Input, merge, ZeroPadding2D, Concatenate
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import AveragePooling2D, GlobalAveragePooling2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization

import six
from keras.regularizers import l2
from keras.models import Model
from keras import regularizers

from keras import backend as K
K.set_image_data_format('channels_first')

try:
    from keras import initializations
except ImportError:
    from keras import initializers as initializations
import keras.backend as K



class MODEL(object):

    def __init__(self,config):
        self.config = config
        self.gf = 64
        self.df = 64

    def input_shape_define(self):
        return  (self.config.normal_size, self.config.normal_size, self.config.channles)

    def covn_block(self,model,kenal_number,kenal_size,padding,activation):
        model.add(Convolution2D(kenal_number,kenal_size,padding=padding,activation=activation))
        return model

    def max_pooling_type(self,model,kenal_size,strides):
        model.add(MaxPooling2D(pool_size=kenal_size,strides=strides))
        return model

    def mnist_net(self):
        model = Sequential()
        input_shape = (self.config.normal_size, self.config.normal_size, self.config.channles)
        model.add(Convolution2D(96,(3,3),input_shape=input_shape,padding='same',activation='relu',kernel_initializer='uniform'))
        model.add(Convolution2D(128,(3,3),padding='same',activation='relu'))
        model.add(Convolution2D(128,(1,1),padding='same',activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.add(Convolution2D(256,(3,3),padding='same',activation='relu'))
        model.add(Convolution2D(256,(1,1),padding='same',activation='relu'))
        model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
        model.add(Convolution2D(512, (3, 3), padding='same', activation='relu'))
        model.add(Convolution2D(512, (3, 3), padding='same', activation='relu'))
        model.add(Convolution2D(256, (1, 1), padding='same', activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        model.add(Convolution2D(512, (3, 3), padding='same', activation='relu'))
        model.add(Convolution2D(512, (3, 3), padding='same', activation='relu'))
        model.add(Convolution2D(256, (1, 1), padding='same', activation='relu'))
        # model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        model.add(Flatten())
        # model.add(Dense(4096,activation='relu'))
        model.add(Dense(1024,activation='relu'))
        model.add(Dropout(0.5))
        # model.add(Dense(2048, activation='relu'))
        model.add(Dense(1024, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.config.classNumber,activation='softmax'))
        return model

    #VGG16
    def TSL16(self):
        model = Sequential()
        input_shape = (self.config.channles, self.config.normal_size, self.config.normal_size)
        model.add(Convolution2D(64,kernel_size=(3,3),input_shape=input_shape,padding='same',activation='relu'))
        model.add(Convolution2D(64,kernel_size=(3,3),padding='same',activation='relu'))
        model = self.max_pooling_type(model,kenal_size=(2,2),strides=(2,2))
        for i in range(2):
            model = self.covn_block(model, kenal_number=128, kenal_size=(3, 3), padding='same', activation='relu')

        model = self.max_pooling_type(model,kenal_size = (2,2),strides=(2,2))
        for i in range(3):
            model = self.covn_block(model,kenal_number=128,  kenal_size=(3,3),  padding='same',activation='relu')

        model = self.max_pooling_type(model,kenal_size=(2,2),strides=(2,2))
        for i in range(3):
            model = self.covn_block(model,kenal_number=512,kenal_size=(3,3),padding='same',activation='relu')

        model = self.max_pooling_type(model,kenal_size=(2,2),strides=(2,2))
        for i in range(3):
            model = self.covn_block(model,kenal_number=512,kenal_size=(3,3),padding='same',activation='relu')

        model.add(Flatten())
        # model.add(Dense(4096,activation='relu'))
        model.add(Dense(1024,activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(1024,activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.config.classNumber,activation='softmax'))
        return model

    def DAN(self):
        model = Sequential()
        #input_shape = (2048, 7, 7)
        #model.add(Convolution2D(1024,kernel_size=(3,3),input_shape=input_shape,padding='same',activation='relu'))
        #model = self.max_pooling_type(model, kenal_size=(2, 2), strides=(2, 2))
        #model = self.max_pooling_type(model, kenal_size=(2, 2), strides=(2, 2))
        #model.add(Flatten())
        input_shape = (2048, )
        model.add(Dense(256, input_shape=input_shape, activation='relu'))
        model.add(Dense(128, activation='relu'))
        model.add(BatchNormalization())
        #model.add(Dense(512, activation='relu'))
        #model.add(Dense(512, activation='relu'))
        #model.add(Dense(128, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
    # model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
        return model

    def GAN(self):
        # def d_layer(layer_input, filters, f_size=4, bn=True):
        #     """Discriminator layer"""
        #     d = Conv2D(filters, kernel_size=f_size, strides=2, padding='same')(layer_input)
        #     d = LeakyReLU(alpha=0.2)(d)
        #     if bn:
        #         d = BatchNormalization(momentum=0.8)(d)
        #     return d
        #
        # img_A = Input((self.config.channles, self.config.normal_size, self.config.normal_size))
        #
        # d1 = d_layer(img_A, self.df, bn=False)
        # d2 = d_layer(d1, self.df*2)
        # d3 = d_layer(d2, self.df*4)
        # d4 = d_layer(d3, self.df*8)
        #
        # validity = Conv2D(1, kernel_size=4, strides=1, padding='same')(d4)
        #
        # return Model(img_A, validity)
        model = Sequential()
        input_shape= (self.config.channles, self.config.normal_size, self.config.normal_size)
        model.add(Convolution2D(64,(3,3),input_shape=input_shape,activation='relu',padding='same'))
        model.add(Convolution2D(64,(3,3),activation='relu',padding='same'))
        model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
        model.add(Convolution2D(128,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(128,(3,3),activation='relu',padding='same'))
        model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
        model.add(Convolution2D(64,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(64,(3,3),activation='relu',padding='same'))
        model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
        model.add(Convolution2D(32,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(32,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(1,(3,3),activation='relu',padding='same'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        return model


    def UNet(self):
        def conv2d(layer_input, filters, f_size=4, bn=True):
            """Layers used during downsampling"""
            d = Conv2D(filters, kernel_size=f_size, strides=2, padding='same')(layer_input)
            d = LeakyReLU(alpha=0.2)(d)
            if bn:
                d = BatchNormalization(momentum=0.8)(d)
            return d

        def deconv2d(layer_input, skip_input, filters, f_size=4, dropout_rate=0):
            """Layers used during upsampling"""
            u = UpSampling2D(size=2)(layer_input)
            u = Conv2D(filters, kernel_size=f_size, strides=1, padding='same', activation='relu')(u)
            if dropout_rate:
                u = Dropout(dropout_rate)(u)
            u = BatchNormalization(momentum=0.8)(u)
            u = Concatenate(axis=1)([u, skip_input])
            return u

        # Image input
        d0 = Input((self.config.channles, self.config.normal_size, self.config.normal_size))

        # Downsampling
        d1 = conv2d(d0, self.gf, bn=False)
        d2 = conv2d(d1, self.gf*2)
        d3 = conv2d(d2, self.gf*4)
        d4 = conv2d(d3, self.gf*8)
        d5 = conv2d(d4, self.gf*8)
        d6 = conv2d(d5, self.gf*8)
        d7 = conv2d(d6, self.gf*8)

        # Upsampling
        u1 = deconv2d(d7, d6, self.gf*8)
        u2 = deconv2d(u1, d5, self.gf*8)
        u3 = deconv2d(u2, d4, self.gf*8)
        u4 = deconv2d(u3, d3, self.gf*4)
        u5 = deconv2d(u4, d2, self.gf*2)
        u6 = deconv2d(u5, d1, self.gf)

        u7 = UpSampling2D(size=2)(u6)
        output_img = Conv2D(self.config.channles, kernel_size=4, strides=1, padding='same', activation='tanh')(u7)
        return Model(d0, output_img)

    # AlexNet
    def AlexNet(self):
        model = Sequential()
        # input_shape = (64,64, self.config.channles)
        input_shape = Input((self.config.channles, self.config.normal_size, self.config.normal_size))
        model.add(Convolution2D(96, (11, 11), input_shape=input_shape,strides=(4, 4),  padding='valid',activation='relu', kernel_initializer='uniform'))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))#26*26
        model.add(Convolution2D(256, (5, 5), strides=(1, 1), padding='same', activation='relu', kernel_initializer='uniform'))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
        model.add(Convolution2D(384, (3, 3), strides=(1, 1), padding='same', activation='relu', kernel_initializer='uniform'))
        #model.add(Convolution2D(384, (3, 3), strides=(1, 1), padding='same', activation='relu', kernel_initializer='uniform'))
        model.add(Convolution2D(256, (3, 3), strides=(1, 1), padding='same', activation='relu', kernel_initializer='uniform'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.add(Flatten())
        # model.add(Dense(4096, activation='relu'))
        model.add(Dense(1024, activation='relu'))
        model.add(Dropout(0.5))
        # model.add(Dense(4096, activation='relu'))
        model.add(Dense(1024, activation='relu'))
        #model.add(Dropout(0.5))
        model.add(Dense(1, activation='sigmoid'))
        # model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
        return model

    def VGG16(self):
        model = Sequential()
        input_shape= (self.config.channles, self.config.normal_size, self.config.normal_size)
        model.add(Convolution2D(64,(3,3),input_shape=input_shape,activation='relu',padding='same'))
        model.add(Convolution2D(64,(3,3),activation='relu',padding='same'))
        model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
        model.add(Convolution2D(128,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(128,(3,3),activation='relu',padding='same'))
        model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
        model.add(Convolution2D(256,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(256,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(256,(3,3),activation='relu',padding='same'))
        model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
        model.add(Convolution2D(512,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(512,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(512,(3,3),activation='relu',padding='same'))
        model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
        model.add(Convolution2D(512,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(512,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(512,(3,3),activation='relu',padding='same'))
        model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
        model.add(Flatten())
        model.add(Dense(1024,activation='relu'))
        model.add(Dense(1024,activation='relu',name='feature'))
        model.add(Dense(1,activation='sigmoid'))
        return model

    def VGG19(self):
        model = Sequential()
        input_shape= (self.config.normal_size, self.config.normal_size, self.config.channles)
        model.add(Convolution2D(64,(3,3),input_shape=input_shape,activation='relu',padding='same'))
        model.add(Convolution2D(64,(3,3),activation='relu',padding='same'))
        model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
        model.add(Convolution2D(128,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(128,(3,3),activation='relu',padding='same'))
        model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
        model.add(Convolution2D(256,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(256,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(256,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(256,(3,3),activation='relu',padding='same'))
        model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
        model.add(Convolution2D(512,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(512,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(512,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(512,(3,3),activation='relu',padding='same'))
        model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
        model.add(Convolution2D(512,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(512,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(512,(3,3),activation='relu',padding='same'))
        model.add(Convolution2D(512,(3,3),activation='relu',padding='same'))
        model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
        model.add(Flatten())
        model.add(Dense(1024,activation='relu'))
        model.add(Dense(1024,activation='relu'))
        model.add(Dense(self.config.classNumber,activation='softmax'))
        return model

    #LeNet
    def LeNet(self):
        # initialize the model
        model = Sequential()
        inputShape = (self.config.channles, self.config.normal_size, self.config.normal_size)
        model.add(Conv2D(20, (5, 5), padding="same", input_shape=inputShape))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        # second set of CONV => RELU => POOL layers
        model.add(Conv2D(50, (5, 5), padding="same"))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        # first (and only) set of FC => RELU layers
        model.add(Flatten())
        model.add(Dense(500))
        #model.add(Dropout(0.5))
        model.add(Activation("relu"))

        # softmax classifier
        model.add(Dense(self.config.classNumber))
        model.add(Activation("softmax"))
        model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
        # return the constructed network architecture
        return model

    #ZF_Net,8 layers
    def ZF_Net(self):
        model = Sequential()
        model.add(
            Conv2D(96, (7, 7), strides=(2, 2),
                   input_shape=(self.config.normal_size, self.config.normal_size,self.config.channles),
                   padding='valid',
                   activation='relu',
                   kernel_initializer='uniform'))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
        model.add(Conv2D(256, (5, 5), strides=(2, 2), padding='same', activation='relu', kernel_initializer='uniform'))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
        model.add(Conv2D(384, (3, 3), strides=(1, 1), padding='same', activation='relu', kernel_initializer='uniform'))
        model.add(Conv2D(384, (3, 3), strides=(1, 1), padding='same', activation='relu', kernel_initializer='uniform'))
        model.add(Conv2D(256, (3, 3), strides=(1, 1), padding='same', activation='relu', kernel_initializer='uniform'))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
        model.add(Flatten())
        model.add(Dense(4096, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(4096, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.config.classNumber, activation='softmax'))
        model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
        return model

#RESNET
class ResnetBuilder(object):
    # @staticmethod
    def build(self,config, block_fn, repetitions, domain=False):
        """Builds a custom ResNet like architecture.
        Args:
            input_shape: The input shape in the form (nb_channels, nb_rows, nb_cols)
            num_outputs: The number of outputs at final softmax layer
            block_fn: The block function to use. This is either `basic_block` or `bottleneck`.
                The original paper used basic_block for layers < 50
            repetitions: Number of repetitions of various block units.
                At each block unit, the number of filters are doubled and the input size is halved
        Returns:
            The keras `Model`.
        """

        input_shape = (config.channles, config.normal_size, config.normal_size)
        if domain:
            num_outputs = 1
        else:
            num_outputs = config.classNumber
        self._handle_dim_ordering()
        block_fn = self._get_block(block_fn)

        input = Input(shape=input_shape)
        conv1 = self._conv_bn_relu(filters=64, kernel_size=(7, 7), strides=(2, 2))(input)
        pool1 = MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding="same")(conv1)

        block = pool1
        filters = 64
        for i, r in enumerate(repetitions):
            block = self._residual_block(block_fn, filters=filters, repetitions=r, is_first_layer=(i == 0))(block)
            filters *= 2

        # Last activation
        block = self._bn_relu(block)

        # Classifier block
        block_shape = K.int_shape(block)
        pool2 = AveragePooling2D(pool_size=(block_shape[ROW_AXIS], block_shape[COL_AXIS]),
                                 strides=(1, 1))(block)

        flatten1 = Flatten(name='feature')(pool2)
        if domain:
            dense = Dense(units=num_outputs,
                      activation="sigmoid")(flatten1)
        else:
            dense = Dense(units=num_outputs,
                      activation="softmax")(flatten1)

        model = Model(inputs=input, outputs=dense)
        # model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
        return model

    # @staticmethod
    def build_resnet18(self, params, domain):
        return self.build(params, self.basic_block, [2, 2, 2, 2], domain)

    # @staticmethod
    def build_resnet34(self,params):
        return self.build(params, self.basic_block, [3, 4, 6, 3])

    # @staticmethod
    def build_resnet50(self,params):
        return self.build(params, self.bottleneck, [3, 4, 6, 3])

    # @staticmethod
    def build_resnet101(self,params):
        return self.build(params, self.bottleneck, [3, 4, 23, 3])

    # @staticmethod
    def build_resnet152(self,params):
        return self.build(params, self.bottleneck, [3, 8, 36, 3])

    def _bn_relu(self,input):
        """Helper to build a BN -> relu block
        """
        norm = BatchNormalization(axis=CHANNEL_AXIS)(input)
        return Activation("relu")(norm)

    def _conv_bn_relu(self,**conv_params):
        """Helper to build a conv -> BN -> relu block
        """
        filters = conv_params["filters"]
        kernel_size = conv_params["kernel_size"]
        strides = conv_params.setdefault("strides", (1, 1))
        kernel_initializer = conv_params.setdefault("kernel_initializer", "he_normal")
        padding = conv_params.setdefault("padding", "same")
        kernel_regularizer = conv_params.setdefault("kernel_regularizer", l2(1.e-4))

        def f(input):
            conv = Conv2D(filters=filters, kernel_size=kernel_size,
                          strides=strides, padding=padding,
                          kernel_initializer=kernel_initializer,
                          kernel_regularizer=kernel_regularizer)(input)
            return self._bn_relu(conv)

        return f


    def _bn_relu_conv(self,**conv_params):
        """Helper to build a BN -> relu -> conv block.
        This is an improved scheme proposed in http://arxiv.org/pdf/1603.05027v2.pdf
        """
        filters = conv_params["filters"]
        kernel_size = conv_params["kernel_size"]
        strides = conv_params.setdefault("strides", (1, 1))
        kernel_initializer = conv_params.setdefault("kernel_initializer", "he_normal")
        padding = conv_params.setdefault("padding", "same")
        kernel_regularizer = conv_params.setdefault("kernel_regularizer", l2(1.e-4))

        def f(input):
            activation = self._bn_relu(input)
            return Conv2D(filters=filters, kernel_size=kernel_size,
                          strides=strides, padding=padding,
                          kernel_initializer=kernel_initializer,
                          kernel_regularizer=kernel_regularizer)(activation)

        return f


    def _shortcut(self,input, residual):
        """Adds a shortcut between input and residual block and merges them with "sum"
        """
        # Expand channles of shortcut to match residual.
        # Stride appropriately to match residual (width, height)
        # Should be int if network architecture is correctly configured.
        input_shape = K.int_shape(input)
        residual_shape = K.int_shape(residual)
        stride_width = int(round(input_shape[ROW_AXIS] / residual_shape[ROW_AXIS]))
        stride_height = int(round(input_shape[COL_AXIS] / residual_shape[COL_AXIS]))
        equal_channels = input_shape[CHANNEL_AXIS] == residual_shape[CHANNEL_AXIS]

        shortcut = input
        # 1 X 1 conv if shape is different. Else identity.
        if stride_width > 1 or stride_height > 1 or not equal_channels:
            shortcut = Conv2D(filters=residual_shape[CHANNEL_AXIS],
                              kernel_size=(1, 1),
                              strides=(stride_width, stride_height),
                              padding="valid",
                              kernel_initializer="he_normal",
                              kernel_regularizer=l2(0.0001))(input)

        return add([shortcut, residual])


    def _residual_block(self,block_function, filters, repetitions, is_first_layer=False):
        """Builds a residual block with repeating bottleneck blocks.
        """
        def f(input):
            for i in range(repetitions):
                init_strides = (1, 1)
                if i == 0 and not is_first_layer:
                    init_strides = (2, 2)
                input = block_function(filters=filters, init_strides=init_strides,
                                       is_first_block_of_first_layer=(is_first_layer and i == 0))(input)
            return input

        return f


    def basic_block(self,filters, init_strides=(1, 1), is_first_block_of_first_layer=False):
        """Basic 3 X 3 convolution blocks for use on resnets with layers <= 34.
        Follows improved proposed scheme in http://arxiv.org/pdf/1603.05027v2.pdf
        """
        def f(input):

            if is_first_block_of_first_layer:
                # don't repeat bn->relu since we just did bn->relu->maxpool
                conv1 = Conv2D(filters=filters, kernel_size=(3, 3),
                               strides=init_strides,
                               padding="same",
                               kernel_initializer="he_normal",
                               kernel_regularizer=l2(1e-4))(input)
            else:
                conv1 = self._bn_relu_conv(filters=filters, kernel_size=(3, 3),
                                      strides=init_strides)(input)

            residual = self._bn_relu_conv(filters=filters, kernel_size=(3, 3))(conv1)
            return self._shortcut(input, residual)

        return f


    def bottleneck(self,filters, init_strides=(1, 1), is_first_block_of_first_layer=False):
        """Bottleneck architecture for > 34 layer resnet.
        Follows improved proposed scheme in http://arxiv.org/pdf/1603.05027v2.pdf
        Returns:
            A final conv layer of filters * 4
        """
        def f(input):

            if is_first_block_of_first_layer:
                # don't repeat bn->relu since we just did bn->relu->maxpool
                conv_1_1 = Conv2D(filters=filters, kernel_size=(1, 1),
                                  strides=init_strides,
                                  padding="same",
                                  kernel_initializer="he_normal",
                                  kernel_regularizer=l2(1e-4))(input)
            else:
                conv_1_1 = self._bn_relu_conv(filters=filters, kernel_size=(1, 1),
                                         strides=init_strides)(input)

            conv_3_3 = self._bn_relu_conv(filters=filters, kernel_size=(3, 3))(conv_1_1)
            residual = self._bn_relu_conv(filters=filters * 4, kernel_size=(1, 1))(conv_3_3)
            return self._shortcut(input, residual)

        return f

    def _handle_dim_ordering(self):
        global ROW_AXIS
        global COL_AXIS
        global CHANNEL_AXIS
        if K.image_data_format() == 'tf':
            ROW_AXIS = 1
            COL_AXIS = 2
            CHANNEL_AXIS = 3
        else:
            CHANNEL_AXIS = 1
            ROW_AXIS = 2
            COL_AXIS = 3

    def _get_block(self,identifier):
        if isinstance(identifier, six.string_types):
            res = globals().get(identifier)
            if not res:
                raise ValueError('Invalid {}'.format(identifier))
            return res
        return identifier