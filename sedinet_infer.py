
## Written by Daniel Buscombe,
## MARDA Science
## daniel@mardascience.com

##> Release v1.3 (July 2020)

from sedinet_models import *

###===================================================
def run_training_siso_simo(vars, train_csvfile, test_csvfile, name, res_folder,
                           mode, greyscale, dropout, numclass, scale):
   """
   This function generates, trains and evaluates a sedinet model for
   continuous prediction
   """

   if numclass>0:
      ID_MAP = dict(zip(np.arange(numclass), [str(k) for k in range(numclass)]))

   ##======================================
   ## this randomly selects imagery for training and testing imagery sets
   ## while also making sure that both training and tetsing sets have
   ## at least 3 examples of each category
   train_idx, train_df = get_df(train_csvfile)
   test_idx, test_df = get_df(test_csvfile)

   ##==============================================
   ## create a sedinet model to estimate category
   if numclass>0:
      SM = make_cat_sedinet(ID_MAP, dropout, greyscale)
   else:
      SM = make_sedinet_siso_simo(vars, greyscale, dropout)

      if scale==True:
          CS = []
          for var in vars:
             cs = RobustScaler() ##alternative = MinMaxScaler()
             cs.fit_transform(
                np.r_[train_df[var].values, test_df[var].values].reshape(-1,1)
                )
             CS.append(cs)
             del cs
      else:
          CS = []

   ##==============================================
   ## train model
   if numclass==0:
      if type(BATCH_SIZE)==list:
         SMs = []; weights_path = []
         for batch_size, valid_batch_size in zip(BATCH_SIZE, VALID_BATCH_SIZE):
            sm, wp = train_sedinet_siso_simo(SM, train_df, test_df,
                                                  train_idx, test_idx, name,
                                                  vars, mode, greyscale, CS,
                                                  dropout, batch_size, valid_batch_size,
                                                  res_folder, scale)
            SMs.append(sm)
            weights_path.append(wp)
            gc.collect()

      else:
         SM, weights_path = train_sedinet_siso_simo(SM, train_df, test_df,
                                                  train_idx, test_idx, name,
                                                  vars, mode, greyscale, CS,
                                                  dropout, BATCH_SIZE, VALID_BATCH_SIZE,
                                                  res_folder, scale)
   else:
      if type(BATCH_SIZE)==list:
         SMs = []; weights_path = []
         for batch_size, valid_batch_size in zip(BATCH_SIZE, VALID_BATCH_SIZE):
            sm, wp = train_sedinet_cat(SM, train_df, test_df, train_idx,
                         test_idx, ID_MAP, vars, greyscale, name, mode,
                         batch_size, valid_batch_size, res_folder)
            SMs.append(sm)
            weights_path.append(wp)
            gc.collect()

      else:
          SM, weights_path = train_sedinet_cat(SM, train_df, test_df, train_idx,
                         test_idx, ID_MAP, vars, greyscale, name, mode,
                         BATCH_SIZE, VALID_BATCH_SIZE, res_folder)


      classes = np.arange(len(ID_MAP))

   K.clear_session()

   # classes = [i for i in ID_MAP.keys()]
   # SM = SMs
   # var = vars[0]
   ##==============================================
   # test model
   if numclass==0:
      if type(BATCH_SIZE)==list:
          predict_test_train_siso_simo(train_df, test_df, train_idx, test_idx, vars,
                                SMs, weights_path, name, mode, greyscale, CS,
                                dropout, scale, DO_AUG)
      else:
          predict_test_train_siso_simo(train_df, test_df, train_idx, test_idx, vars,
                                SM, weights_path, name, mode, greyscale, CS,
                                dropout, scale, DO_AUG)

   else:
      if type(BATCH_SIZE)==list:
          predict_test_train_cat(train_df, test_df, train_idx, test_idx, vars[0],
                             SMs, [i for i in ID_MAP.keys()], weights_path, greyscale,
                             name, DO_AUG)
      else:
          predict_test_train_cat(train_df, test_df, train_idx, test_idx, vars[0],
                             SM, [i for i in ID_MAP.keys()], weights_path, greyscale,
                             name, DO_AUG)

   K.clear_session()

   ##===================================
   ## move model files and plots to the results folder
   tidy(name, res_folder)


# df = train_df
# indices=train_idx[:10]
# for_training=True

###==================================
def train_sedinet_cat(SM, train_df, test_df, train_idx, test_idx,
                      ID_MAP, vars, greyscale, name, mode, batch_size, valid_batch_size,
                      res_folder):
    """
    This function trains an implementation of SediNet
    """
    ##================================
    ## create training and testing file generators, set the weights path,
    ## plot the model, and create a callback list for model training
    train_gen = get_data_generator_1image(train_df, train_idx, True, ID_MAP,
                vars[0], batch_size, greyscale, DO_AUG) ##BATCH_SIZE
    valid_gen = get_data_generator_1image(test_df, test_idx, True, ID_MAP,
                vars[0], valid_batch_size, greyscale, False) ##VALID_BATCH_SIZE

    if SHALLOW is True:
       if DO_AUG is True:
           weights_path = name+"_"+mode+"_batch"+str(batch_size)+"_im"+str(IM_HEIGHT)+\
                   "_"+str(IM_WIDTH)+"_shallow_"+vars[0]+"_"+CAT_LOSS+"_aug.hdf5"
       else:
           weights_path = name+"_"+mode+"_batch"+str(batch_size)+"_im"+str(IM_HEIGHT)+\
                   "_"+str(IM_WIDTH)+"_shallow_"+vars[0]+"_"+CAT_LOSS+"_noaug.hdf5"
    else:
       if DO_AUG is True:
           weights_path = name+"_"+mode+"_batch"+str(batch_size)+"_im"+str(IM_HEIGHT)+\
                   "_"+str(IM_WIDTH)+"_"+vars[0]+"_"+CAT_LOSS+"_aug.hdf5"
       else:
           weights_path = name+"_"+mode+"_batch"+str(batch_size)+"_im"+str(IM_HEIGHT)+\
                   "_"+str(IM_WIDTH)+"_"+vars[0]+"_"+CAT_LOSS+"_noaug.hdf5"

    if os.path.exists(weights_path):
        SM.load_weights(weights_path)
        print("==========================================")
        print("Loading weights that already exist: %s" % (weights_path)  )
        print("Skipping model training")

    elif os.path.exists(res_folder+os.sep+weights_path):
        weights_path = res_folder+os.sep+weights_path
        SM.load_weights(weights_path)
        print("==========================================")
        print("Loading weights that already exist: %s" % (weights_path)  )
        print("Skipping model training")

    else:

        try:
           plot_model(SM, weights_path.replace('.hdf5', '_model.png'),
                      show_shapes=True, show_layer_names=True)
        except:
           pass

        callbacks_list = [
             ModelCheckpoint(weights_path, monitor='val_loss', verbose=1,
                             save_best_only=True, mode='min',
                             save_weights_only = True)
         ]

        print("=========================================")
        print("[INFORMATION] schematic of the model has been written out to: "+\
              weights_path.replace('.hdf5', '_model.png'))
        print("[INFORMATION] weights will be written out to: "+weights_path)

        ##==============================================
        ## set checkpoint file and parameters that control early stopping,
        ## and reduction of learning rate if and when validation
        ## scores plateau upon successive epochs
        # reduceloss_plat = ReduceLROnPlateau(monitor='val_loss', factor=FACTOR,
        #                   patience=STOP_PATIENCE, verbose=1, mode='auto', min_delta=MIN_DELTA,
        #                   cooldown=STOP_PATIENCE, min_lr=MIN_LR)
        #
        # earlystop = EarlyStopping(monitor="val_loss", mode="min", patience=STOP_PATIENCE)

        model_checkpoint = ModelCheckpoint(weights_path, monitor='val_loss',
                           verbose=1, save_best_only=True, mode='min',
                           save_weights_only = True)

        #tqdm_callback = tfa.callbacks.TQDMProgressBar()
        # callbacks_list = [model_checkpoint, reduceloss_plat, earlystop] #, tqdm_callback]

        ##==============================================
        ## train the model
        # history = SM.fit(train_gen,
        #                 steps_per_epoch=len(train_idx)//batch_size, ##BATCH_SIZE
        #                 epochs=NUM_EPOCHS,
        #                 callbacks=callbacks_list,
        #                 validation_data=valid_gen, #use_multiprocessing=True,
        #                 validation_steps=len(test_idx)//valid_batch_size) #max_queue_size=10 ##VALID_BATCH_SIZE

        ## with non-adaptive exponentially decreasing learning rate
        exponential_decay_fn = exponential_decay(MAX_LR, NUM_EPOCHS)

        lr_scheduler = LearningRateScheduler(exponential_decay_fn)

        callbacks_list = [model_checkpoint, lr_scheduler]

        ## train the model
        history = SM.fit(train_gen,
                        steps_per_epoch=len(train_idx)//batch_size, ##BATCH_SIZE
                        epochs=NUM_EPOCHS,
                        callbacks=callbacks_list,
                        validation_data=valid_gen, #use_multiprocessing=True,
                        validation_steps=len(test_idx)//valid_batch_size) #max_queue_size=10 ##VALID_BATCH_SIZE

        ###===================================================
        ## Plot the loss and accuracy as a function of epoch
        plot_train_history_1var(history)
        # plt.savefig(vars+'_'+str(IM_HEIGHT)+'_batch'+str(batch_size)+'_history.png', ##BATCH_SIZE
        #             dpi=300, bbox_inches='tight')
        plt.savefig(weights_path.replace('.hdf5','_history.png'),dpi=300, bbox_inches='tight')
        plt.close('all')

        # serialize model to JSON to use later to predict
        model_json = SM.to_json()
        with open(weights_path.replace('.hdf5','.json'), "w") as json_file:
           json_file.write(model_json)

    return SM, weights_path

###===================================================
def train_sedinet_siso_simo(SM, train_df, test_df, train_idx, test_idx, name,
                            vars, mode, greyscale, CS, dropout, batch_size, valid_batch_size,
                            res_folder, scale):
    """
    This function trains an implementation of sedinet
    """

    ##==============================================
    ## create training and testing file generators, set the weights path,
    ## plot the model, and create a callback list for model training

    train_gen = get_data_generator_Nvars_siso_simo(train_df, train_idx, True,
                                                   vars, batch_size, greyscale, CS, DO_AUG)
    valid_gen = get_data_generator_Nvars_siso_simo(test_df, test_idx, True,
                                                   vars, valid_batch_size, greyscale, CS, False) ##only augment training

    # get a string saying how many variables, fr the output files
    varstring = str(len(vars))+'vars' #''.join([str(k)+'_' for k in vars])

    # mae the appropriate weights file
    if SHALLOW is True:
       if DO_AUG is True:
          if scale is True:
              weights_path = name+"_"+mode+"_batch"+str(batch_size)+"_im"+str(IM_HEIGHT)+\
                   "_"+str(IM_WIDTH)+"_shallow_"+varstring+"_"+CONT_LOSS+"_aug_scale.hdf5"
          else:
              weights_path = name+"_"+mode+"_batch"+str(batch_size)+"_im"+str(IM_HEIGHT)+\
                   "_"+str(IM_WIDTH)+"_shallow_"+varstring+"_"+CONT_LOSS+"_aug.hdf5"
       else:
          if scale is True:
              weights_path = name+"_"+mode+"_batch"+str(batch_size)+"_im"+str(IM_HEIGHT)+\
                   "_"+str(IM_WIDTH)+"_shallow_"+varstring+"_"+CONT_LOSS+"_noaug_scale.hdf5"
          else:
              weights_path = name+"_"+mode+"_batch"+str(batch_size)+"_im"+str(IM_HEIGHT)+\
                   "_"+str(IM_WIDTH)+"_shallow_"+varstring+"_"+CONT_LOSS+"_noaug.hdf5"
    else:
       if DO_AUG is True:
          if scale is True:
              weights_path = name+"_"+mode+"_batch"+str(batch_size)+"_im"+str(IM_HEIGHT)+\
                   "_"+str(IM_WIDTH)+"_"+varstring+"_"+CONT_LOSS+"_aug_scale.hdf5"
          else:
              weights_path = name+"_"+mode+"_batch"+str(batch_size)+"_im"+str(IM_HEIGHT)+\
                   "_"+str(IM_WIDTH)+"_"+varstring+"_"+CONT_LOSS+"_aug.hdf5"
       else:
          if scale is True:
              weights_path = name+"_"+mode+"_batch"+str(batch_size)+"_im"+str(IM_HEIGHT)+\
                   "_"+str(IM_WIDTH)+"_"+varstring+"_"+CONT_LOSS+"_noaug_scale.hdf5"
          else:
              weights_path = name+"_"+mode+"_batch"+str(batch_size)+"_im"+str(IM_HEIGHT)+\
                   "_"+str(IM_WIDTH)+"_"+varstring+"_"+CONT_LOSS+"_noaug.hdf5"

    # if it already exists, skip training
    if os.path.exists(weights_path):
        SM.load_weights(weights_path)
        print("==========================================")
        print("Loading weights that already exist: %s" % (weights_path)  )
        print("Skipping model training")

    # if it already exists in res_folder, skip training
    elif os.path.exists(res_folder+os.sep+weights_path):
        weights_path = res_folder+os.sep+weights_path
        SM.load_weights(weights_path)
        print("==========================================")
        print("Loading weights that already exist: %s" % (weights_path)  )
        print("Skipping model training")

    else: #train

        # if scaler=true (CS=[]), dump out scalers to pickle file
        if len(CS)==0:
            pass
        else:
            joblib.dump(CS, weights_path.replace('.hdf5','_scaler.pkl'))

        try: # plot the model if pydot/graphviz installed
            plot_model(SM, weights_path.replace('.hdf5', '_model.png'),
                       show_shapes=True, show_layer_names=True)
            print("[INFORMATION] model schematic written to: "+\
                  weights_path.replace('.hdf5', '_model.png'))
        except:
            pass

        print("==========================================")
        print("[INFORMATION] weights will be written out to: "+weights_path)

        ##==============================================
        ## set checkpoint file and parameters that control early stopping,
        ## and reduction of learning rate if and when validation scores plateau upon successive epochs
        # reduceloss_plat = ReduceLROnPlateau(monitor='val_loss', factor=FACTOR,
        #                                     patience=STOP_PATIENCE, verbose=1, mode='auto',
        #                                     min_delta=MIN_DELTA, cooldown=5,
        #                                     min_lr=MIN_LR)
        #
        # earlystop = EarlyStopping(monitor="val_loss", mode="min",
        #                           patience=STOP_PATIENCE)

        # set model checkpoint. only save best weights, based on min validation loss
        model_checkpoint = ModelCheckpoint(weights_path, monitor='val_loss', verbose=1,
                                           save_best_only=True, mode='min',
                                           save_weights_only = True)


        #tqdm_callback = tfa.callbacks.TQDMProgressBar()
        # callbacks_list = [model_checkpoint, reduceloss_plat, earlystop] #, tqdm_callback]

        try: #write summary of the model to txt file
            with open(weights_path.replace('.hdf5','') + '_report.txt','w') as fh:
                # Pass the file handle in as a lambda function to make it callable
                SM.summary(print_fn=lambda x: fh.write(x + '\n'))
            fh.close()
            print("[INFORMATION] model summary written to: "+ \
                  weights_path.replace('.hdf5','') + '_report.txt')
            with open(weights_path.replace('.hdf5','') + '_report.txt','r') as fh:
                tmp = fh.readlines()
            print("===============================================")
            print("Total parameters: %s" %\
                 (''.join(tmp).split('Total params:')[-1].split('\n')[0]))
            fh.close()
            print("===============================================")
        except:
            pass

        ##==============================================
        ## train the model
        # history = SM.fit(train_gen,
        #                 steps_per_epoch=len(train_idx)//batch_size, ##BATCH_SIZE
        #                 epochs=NUM_EPOCHS,
        #                 callbacks=callbacks_list,
        #                 validation_data=valid_gen,
        #                 validation_steps=len(test_idx)//valid_batch_size) ##VALID_BATCH_SIZE
        #                 #use_multiprocessing=True

        ## non-adaptive exponentially decreasing learning rate
        exponential_decay_fn = exponential_decay(MAX_LR, NUM_EPOCHS)

        lr_scheduler = LearningRateScheduler(exponential_decay_fn)

        callbacks_list = [model_checkpoint, lr_scheduler]

        ## train the model
        history = SM.fit(train_gen,
                        steps_per_epoch=len(train_idx)//batch_size, ##BATCH_SIZE
                        epochs=NUM_EPOCHS,
                        callbacks=callbacks_list,
                        validation_data=valid_gen, #use_multiprocessing=True,
                        validation_steps=len(test_idx)//valid_batch_size) #max_queue_size=10 ##VALID_BATCH_SIZE


        ###===================================================
        ## Plot the loss and accuracy as a function of epoch
        if len(vars)==1:
           plot_train_history_1var_mae(history)
        else:
           plot_train_history_Nvar(history, vars, len(vars))

        varstring = ''.join([str(k)+'_' for k in vars])
        plt.savefig(weights_path.replace('.hdf5', '_history.png'), dpi=300,
                    bbox_inches='tight')
        plt.close('all')

        # serialize model to JSON to use later to predict
        model_json = SM.to_json()
        with open(weights_path.replace('.hdf5','.json'), "w") as json_file:
           json_file.write(model_json)

    return SM, weights_path

#
# ###===================================================
# def run_training_miso_mimo(vars, train_csvfile, test_csvfile, name, res_folder,
#                            mode, greyscale, auxin, dropout):
#    """
#    This function generates, trains and evaluates a sedinet model for
#    continuous prediction
#    """
#    ##======================================
#    ## this randomly selects imagery for training and testing imagery sets
#    ## while also making sure that both training and tetsing sets
#    ## have at least 3 examples of each category
#    train_idx, train_df = get_df(train_csvfile)
#    test_idx, test_df = get_df(test_csvfile)
#
#    ##==============================================
#    ## create a sedinet model to estimate category
#    cnn = make_sedinet_miso_mimo(False, dropout)
#
#    CS = []
#    for var in vars:
#       cs = RobustScaler() #MinMaxScaler()
#       cs.fit_transform(
#          np.r_[train_df[var].values, test_df[var].values].reshape(-1,1)
#          )
#       CS.append(cs)
#       del cs
#
#    CSaux = []
#    cs = RobustScaler() #MinMaxScaler()
#    cs.fit_transform(
#        np.r_[train_df[auxin].values, test_df[auxin].values].reshape(-1,1)
#        )
#    CSaux.append(cs)
#    del cs
#
#    ##==============================================
#    ## train model
#    if type(BATCH_SIZE)==list:
#        # SM, weights_path = train_sedinet_miso_mimo(cnn, train_df, test_df,
#        #                                                train_idx, test_idx, name, vars,
#        #                                                auxin, mode, greyscale,
#        #                                                CS, CSaux)
#       SMs = []; weights_path = []
#       for batch_size, valid_batch_size in zip(BATCH_SIZE, VALID_BATCH_SIZE):
#          sm, wp = train_sedinet_miso_mimo(cnn, train_df, test_df,
#                                               train_idx, test_idx, name,
#                                               vars, auxin, mode, greyscale, CS, CSaux,
#                                               batch_size, valid_batch_size)
#          SMs.append(sm)
#          weights_path.append(wp)
#    else:
#       SM, weights_path = train_sedinet_miso_mimo(cnn, train_df, test_df,
#                                                       train_idx, test_idx, name, vars,
#                                                       auxin, mode, greyscale,
#                                                       CS, CSaux)
#
#    if type(BATCH_SIZE)==list:
#        # test model
#        predict_test_train_miso_mimo(train_df, test_df, train_idx, test_idx, vars,
#                                     auxin, SMs, weights_path, name, mode,
#                                     greyscale, CS, CSaux)
#
#    else:
#        predict_test_train_miso_mimo(train_df, test_df, train_idx, test_idx, vars,
#                                     auxin, SM, weights_path, name, mode,
#                                     greyscale, CS, CSaux)
#
#    K.clear_session()
#
#    ##==============================================
#    ## move model files and plots to the results folder
#    tidy(res_folder)#, name)
#
# ###===================================================
# def train_sedinet_miso_mimo(cnn, train_df, test_df, train_idx, test_idx,
#                             name, vars, auxin, mode, greyscale, CS, CSaux):
#     """
#     This function trains an implementation of sedinet
#     """
#
#     dense_neurons = 4
#
#     ##==============================================
#     ## create training and testing file generators,
#     # set the weights path, plot the model, and create
#     # a callback list for model training
#     varstring = ''.join([str(k)+'_' for k in vars])
#     weights_path = name+"_"+auxin+"_"+mode+"_batch"+str(BATCH_SIZE)+"_"+\
#                    varstring+"_checkpoint.hdf5"
#
#     # Create the MLP and CNN models
#     mlp = make_mlp(1) #dense_neurons
#
#     # Create the input to the final set of layers as the output of both the MLP and CNN
#     combinedInput = concatenate([mlp.output, cnn.output])
#
#     # The final fully-connected layer head will have two dense layers
#     # (one relu and one sigmoid)
#     x = Dense(dense_neurons, activation="relu")(combinedInput)
#     x = Dense(1, activation="sigmoid")(x)
#
#     ## The final model accepts numerical data on the MLP input and
#     ## images on the CNN input, outputting a single value
#     outputs = []
#     for var in vars:
#        outputs.append(Dense(units=1, activation='linear', name=var+'_output')(x) )
#
#     loss = dict(zip([k+"_output" for k in vars], ['mse' for k in vars]))
#     metrics = dict(zip([k+"_output" for k in vars], ['mae' for k in vars]))
#
#     # our final model will accept categorical/numerical data on the MLP
#     # input and images on the CNN input
#     SM = Model(inputs=[mlp.input, cnn.input], outputs=outputs)
#
#     SM.compile(optimizer=OPT, loss=loss, metrics=metrics)
#
#     try:
#         plot_model(SM, weights_path.replace('.hdf5', '_model.png'),
#                    show_shapes=True, show_layer_names=True)
#         print("[INFORMATION] model schematic written to: "+\
#               weights_path.replace('.hdf5', '_model.png'))
#     except:
#         pass
#
#     print("==========================================")
#     print("[INFORMATION] weights will be written out to: "+weights_path)
#
#
#     try:
#         with open(weights_path.replace('.hdf5','') + '_report.txt','w') as fh:
#             # Pass the file handle in as a lambda function to make it callable
#             SM.summary(print_fn=lambda x: fh.write(x + '\n'))
#         fh.close()
#         print("[INFORMATION] model summary written to: "+\
#               weights_path.replace('.hdf5','') + '_report.txt')
#         with open(weights_path.replace('.hdf5','') + '_report.txt','r') as fh:
#             tmp = fh.readlines()
#         print("===============================================")
#         print("Total parameters: %s" % (''.join(tmp).split('Total params:')[-1].split('\n')[0]))
#         fh.close()
#         print("===============================================")
#     except:
#         pass
#
#
#     reduceloss_plat = ReduceLROnPlateau(monitor='val_loss', factor=FACTOR, patience=STOP_PATIENCE,
#                                         verbose=1, mode='auto', min_delta=MIN_DELTA,
#                                         cooldown=5, min_lr=MIN_LR)
#
#     earlystop = EarlyStopping(monitor="val_loss", mode="auto",
#                               patience=STOP_PATIENCE)
#
#     model_checkpoint = ModelCheckpoint(weights_path, monitor='val_loss',
#                                        verbose=1,
#                                        save_best_only=True, mode='min',
#                                        save_weights_only = True)
#
#
#     callbacks_list = [model_checkpoint, reduceloss_plat, earlystop]
#
#     #aux_mean = train_df[auxin].mean()
#     #aux_std =  train_df[auxin].std()
#
#     train_gen = get_data_generator_Nvars_miso_mimo(train_df, train_idx, True,
#                                                    vars, auxin, BATCH_SIZE,
#                                                    greyscale, CS, CSaux)
#     valid_gen = get_data_generator_Nvars_miso_mimo(test_df, test_idx, True,
#                                                    vars, auxin, VALID_BATCH_SIZE,
#                                                    greyscale, CS, CSaux)
#
#     ##==============================================
#     ## train the model
#     history = SM.fit(train_gen,
#                     steps_per_epoch=len(train_idx)//BATCH_SIZE,
#                     epochs=NUM_EPOCHS,
#                     callbacks=callbacks_list,
#                     validation_data=valid_gen,
#                     validation_steps=len(test_idx)//VALID_BATCH_SIZE)
#                     #use_multiprocessing=True,
#
#     ###===================================================
#     ## Plot the loss and accuracy as a function of epoch
#     if len(vars)==1:
#        plot_train_history_1var_mae(history)
#     else:
#        plot_train_history_Nvar(history, vars, len(vars))
#
#     varstring = ''.join([str(k)+'_' for k in vars])
#     plt.savefig(weights_path.replace('.hdf5', '_history.png'),
#                 dpi=300, bbox_inches='tight')
#     plt.close('all')
#
#     # serialize model to JSON to use later to predict
#     model_json = SM.to_json()
#     with open(weights_path.replace('.hdf5','.json'), "w") as json_file:
#        json_file.write(model_json)
#
#     ## do some garbage collection
#     #gc.collect()
#
#     return SM, weights_path
