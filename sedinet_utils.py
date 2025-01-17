
## Written by Daniel Buscombe,
## MARDA Science
## daniel@mardascience.com

##> Release v1.3 (July 2020)

from imports import *

###===================================================
## FUNCTIONS FOR LEARNING RATE SCHEDULER

def exponential_decay(lr0, s):
    def exponential_decay_fn(epoch):
        return lr0 * 0.1 **(epoch / s)
    return exponential_decay_fn

###===================================================
## IMAGE AUGMENTATION FUNCTIONS (for DO_AUG=True)

# def clockwise_rotation(image):
#     angle= random.randint(0,180)
#     return rotate(image, -angle)

# def h_flip(image):
#     return  np.fliplr(image)

def v_flip(image):
    return np.flipud(image)

def warp_shift(image):
    shift= random.randint(25,200)
    transform = AffineTransform(translation=(0,shift))
    warp_image = warp(image, transform, mode="wrap")
    return warp_image

def apply_aug(im):
    return [im,v_flip(warp_shift(im))] #, clockwise_rotation(im), h_flip(im)]


###===================================================
### IMAGE BATCH GENERATOR FUNCTIONS

def get_data_generator_Nvars_siso_simo(df, indices, for_training, vars,
                                       batch_size, greyscale, CS, do_aug): ##BATCH_SIZE
    """
    This function generates data for a batch of images and N associated metrics
    """

    ##print(do_aug)

    if len(vars)==1:
       images, p1s = [], []
    elif len(vars)==2:
       images, p1s, p2s = [], [], []
    elif len(vars)==3:
       images, p1s, p2s, p3s = [], [], [], []
    elif len(vars)==4:
       images, p1s, p2s, p3s, p4s = [], [], [], [], []
    elif len(vars)==5:
       images, p1s, p2s, p3s, p4s, p5s = [], [], [], [], [], []
    elif len(vars)==6:
       images, p1s, p2s, p3s, p4s, p5s, p6s =\
        [], [], [], [], [], [], []
    elif len(vars)==7:
       images, p1s, p2s, p3s, p4s, p5s, p6s, p7s =\
        [], [], [], [], [], [], [], []
    elif len(vars)==8:
       images, p1s, p2s, p3s, p4s, p5s, p6s, p7s, p8s =\
        [], [], [], [], [], [], [], [], []
    elif len(vars)==9:
       images, p1s, p2s, p3s, p4s, p5s, p6s, p7s, p8s, p9s =\
        [], [], [], [], [], [], [], [], [], []

    while True:
        for i in indices:
            r = df.iloc[i]
            if len(vars)==1:
               file, p1 = r['files'], r[vars[0]]
            if len(vars)==2:
               file, p1, p2 = r['files'], r[vars[0]], r[vars[1]]
            if len(vars)==3:
               file, p1, p2, p3 = \
               r['files'], r[vars[0]], r[vars[1]], r[vars[2]]
            if len(vars)==4:
               file, p1, p2, p3, p4 = \
               r['files'], r[vars[0]], r[vars[1]], r[vars[2]], r[vars[3]]
            if len(vars)==5:
               file, p1, p2, p3, p4, p5 = \
               r['files'], r[vars[0]], r[vars[1]], r[vars[2]], r[vars[3]], r[vars[4]]
            if len(vars)==6:
               file, p1, p2, p3, p4, p5, p6 = \
               r['files'], r[vars[0]], r[vars[1]], r[vars[2]], r[vars[3]], r[vars[4]], r[vars[5]]
            if len(vars)==7:
               file, p1, p2, p3, p4, p5, p6, p7 = \
               r['files'], r[vars[0]], r[vars[1]], r[vars[2]], r[vars[3]], r[vars[4]], r[vars[5]], r[vars[6]]
            if len(vars)==8:
               file, p1, p2, p3, p4, p5, p6, p7, p8 = \
               r['files'], r[vars[0]], r[vars[1]], r[vars[2]], r[vars[3]], r[vars[4]], r[vars[5]], r[vars[6]], r[vars[7]]
            elif len(vars)==9:
               file, p1, p2, p3, p4, p5, p6, p7, p8, p9 = \
               r['files'], r[vars[0]], r[vars[1]], r[vars[2]], r[vars[3]], r[vars[4]], r[vars[5]], r[vars[6]], r[vars[7]], r[vars[8]]

            if greyscale==True:
               im = Image.open(file).convert('LA')
               im = im.resize((IM_HEIGHT, IM_HEIGHT))
               im = np.array(im)[:,:,0]

            else:
               im = Image.open(file)
               im = im.resize((IM_HEIGHT, IM_HEIGHT))
               im = np.array(im)

            im = np.array(im) / 255.0

            #if np.ndim(im)==2:
            #   im = np.dstack((im, im , im)) ##np.expand_dims(im[:,:,0], axis=2)

            #im = im[:,:,:3]

            if greyscale==True:
               if do_aug==True:
                   aug = apply_aug(im)
                   images.append(aug)
                   if len(vars)==1:
                      p1s.append([p1 for k in range(2)])
                   elif len(vars)==2:
                      p1s.append([p1 for k in range(2)]); p2s.append([p2 for k in range(2)])
                   elif len(vars)==3:
                      p1s.append([p1 for k in range(2)]); p2s.append([p2 for k in range(2)])
                      p3s.append([p3 for k in range(2)]);
                   elif len(vars)==4:
                      p1s.append([p1 for k in range(2)]); p2s.append([p2 for k in range(2)])
                      p3s.append([p3 for k in range(2)]); p4s.append([p4 for k in range(2)])
                   elif len(vars)==5:
                      p1s.append([p1 for k in range(2)]); p2s.append([p2 for k in range(2)])
                      p3s.append([p3 for k in range(2)]); p4s.append([p4 for k in range(2)])
                      p5s.append([p5 for k in range(2)]);
                   elif len(vars)==6:
                      p1s.append([p1 for k in range(2)]); p2s.append([p2 for k in range(2)])
                      p3s.append([p3 for k in range(2)]); p4s.append([p4 for k in range(2)])
                      p5s.append([p5 for k in range(2)]); p6s.append([p6 for k in range(2)])
                   elif len(vars)==7:
                      p1s.append([p1 for k in range(2)]); p2s.append([p2 for k in range(2)])
                      p3s.append([p3 for k in range(2)]); p4s.append([p4 for k in range(2)])
                      p5s.append([p5 for k in range(2)]); p6s.append([p6 for k in range(2)])
                      p7s.append([p7 for k in range(2)]);
                   elif len(vars)==8:
                      p1s.append([p1 for k in range(2)]); p2s.append([p2 for k in range(2)])
                      p3s.append([p3 for k in range(2)]); p4s.append([p4 for k in range(2)])
                      p5s.append([p5 for k in range(2)]); p6s.append([p6 for k in range(2)])
                      p7s.append([p7 for k in range(2)]); p8s.append([p8 for k in range(2)])
                   elif len(vars)==9:
                      p1s.append([p1 for k in range(2)]); p2s.append([p2 for k in range(2)])
                      p3s.append([p3 for k in range(2)]); p4s.append([p4 for k in range(2)])
                      p5s.append([p5 for k in range(2)]); p6s.append([p6 for k in range(2)])
                      p7s.append([p7 for k in range(2)]); p8s.append([p8 for k in range(2)])
                      p9s.append([p9 for k in range(2)])

               else:
                   images.append(np.expand_dims(im, axis=2))
                   if len(vars)==1:
                      p1s.append(p1)
                   elif len(vars)==2:
                      p1s.append(p1); p2s.append(p2)
                   elif len(vars)==3:
                      p1s.append(p1); p2s.append(p2)
                      p3s.append(p3);
                   elif len(vars)==4:
                      p1s.append(p1); p2s.append(p2)
                      p3s.append(p3); p4s.append(p4)
                   elif len(vars)==5:
                      p1s.append(p1); p2s.append(p2)
                      p3s.append(p3); p4s.append(p4)
                      p5s.append(p5);
                   elif len(vars)==6:
                      p1s.append(p1); p2s.append(p2)
                      p3s.append(p3); p4s.append(p4)
                      p5s.append(p5); p6s.append(p6)
                   elif len(vars)==7:
                      p1s.append(p1); p2s.append(p2)
                      p3s.append(p3); p4s.append(p4)
                      p5s.append(p5); p6s.append(p6)
                      p7s.append(p7);
                   elif len(vars)==8:
                      p1s.append(p1); p2s.append(p2)
                      p3s.append(p3); p4s.append(p4)
                      p5s.append(p5); p6s.append(p6)
                      p7s.append(p7); p8s.append(p8)
                   elif len(vars)==9:
                      p1s.append(p1); p2s.append(p2)
                      p3s.append(p3); p4s.append(p4)
                      p5s.append(p5); p6s.append(p6)
                      p7s.append(p7); p8s.append(p8)
                      p9s.append(p9)

            else:
               if do_aug==True:
                   aug = apply_aug(im)
                   images.append(aug)
                   if len(vars)==1:
                      p1s.append([p1 for k in range(2)])
                   elif len(vars)==2:
                      p1s.append([p1 for k in range(2)]); p2s.append([p2 for k in range(2)])
                   elif len(vars)==3:
                      p1s.append([p1 for k in range(2)]); p2s.append([p2 for k in range(2)])
                      p3s.append([p3 for k in range(2)]);
                   elif len(vars)==4:
                      p1s.append([p1 for k in range(2)]); p2s.append([p2 for k in range(2)])
                      p3s.append([p3 for k in range(2)]); p4s.append([p4 for k in range(2)])
                   elif len(vars)==5:
                      p1s.append([p1 for k in range(2)]); p2s.append([p2 for k in range(2)])
                      p3s.append([p3 for k in range(2)]); p4s.append([p4 for k in range(2)])
                      p5s.append([p5 for k in range(2)]);
                   elif len(vars)==6:
                      p1s.append([p1 for k in range(2)]); p2s.append([p2 for k in range(2)])
                      p3s.append([p3 for k in range(2)]); p4s.append([p4 for k in range(2)])
                      p5s.append([p5 for k in range(2)]); p6s.append([p6 for k in range(2)])
                   elif len(vars)==7:
                      p1s.append([p1 for k in range(2)]); p2s.append([p2 for k in range(2)])
                      p3s.append([p3 for k in range(2)]); p4s.append([p4 for k in range(2)])
                      p5s.append([p5 for k in range(2)]); p6s.append([p6 for k in range(2)])
                      p7s.append([p7 for k in range(2)]);
                   elif len(vars)==8:
                      p1s.append([p1 for k in range(2)]); p2s.append([p2 for k in range(2)])
                      p3s.append([p3 for k in range(2)]); p4s.append([p4 for k in range(2)])
                      p5s.append([p5 for k in range(2)]); p6s.append([p6 for k in range(2)])
                      p7s.append([p7 for k in range(2)]); p8s.append([p8 for k in range(2)])
                   elif len(vars)==9:
                      p1s.append([p1 for k in range(2)]); p2s.append([p2 for k in range(2)])
                      p3s.append([p3 for k in range(2)]); p4s.append([p4 for k in range(2)])
                      p5s.append([p5 for k in range(2)]); p6s.append([p6 for k in range(2)])
                      p7s.append([p7 for k in range(2)]); p8s.append([p8 for k in range(2)])
                      p9s.append([p9 for k in range(2)])

               else:
                   images.append(im)
                   if len(vars)==1:
                      p1s.append(p1)
                   elif len(vars)==2:
                      p1s.append(p1); p2s.append(p2)
                   elif len(vars)==3:
                      p1s.append(p1); p2s.append(p2)
                      p3s.append(p3);
                   elif len(vars)==4:
                      p1s.append(p1); p2s.append(p2)
                      p3s.append(p3); p4s.append(p4)
                   elif len(vars)==5:
                      p1s.append(p1); p2s.append(p2)
                      p3s.append(p3); p4s.append(p4)
                      p5s.append(p5);
                   elif len(vars)==6:
                      p1s.append(p1); p2s.append(p2)
                      p3s.append(p3); p4s.append(p4)
                      p5s.append(p5); p6s.append(p6)
                   elif len(vars)==7:
                      p1s.append(p1); p2s.append(p2)
                      p3s.append(p3); p4s.append(p4)
                      p5s.append(p5); p6s.append(p6)
                      p7s.append(p7);
                   elif len(vars)==8:
                      p1s.append(p1); p2s.append(p2)
                      p3s.append(p3); p4s.append(p4)
                      p5s.append(p5); p6s.append(p6)
                      p7s.append(p7); p8s.append(p8)
                   elif len(vars)==9:
                      p1s.append(p1); p2s.append(p2)
                      p3s.append(p3); p4s.append(p4)
                      p5s.append(p5); p6s.append(p6)
                      p7s.append(p7); p8s.append(p8)
                      p9s.append(p9)

            if len(images) >= batch_size:
               if len(vars)==1:
                  if len(CS)==0:
                      p1s = np.squeeze(np.array(p1s))
                  else:
                      p1s = np.squeeze(CS[0].transform(np.array(p1s).reshape(-1, 1)))
                  if do_aug==True:
                     if len(images) >= batch_size:
                        if greyscale==False:
                           images = np.array(np.vstack(images))
                        else:
                           images = np.expand_dims(np.array(np.vstack(images)), axis=-1)
                           p1s = np.expand_dims(np.vstack(p1s).flatten(),axis=-1)
                        yield images,[p1s]
                  else:
                     if len(images) >= batch_size:
                           #p1s = np.expand_dims(np.vstack(p1s).flatten(),axis=-1)
                           yield np.array(images),[np.array(p1s)]
                  images, p1s = [], []

               elif len(vars)==2:
                  if len(CS)==0:
                      p1s = np.squeeze(np.array(p1s))
                      p2s = np.squeeze(np.array(p2s))
                  else:
                      p1s = np.squeeze(CS[0].transform(np.array(p1s).reshape(-1, 1)))
                      p2s = np.squeeze(CS[1].transform(np.array(p2s).reshape(-1, 1)))
                  if do_aug==True:
                     if len(images) >= batch_size:
                        if greyscale==False:
                           images = np.array(np.vstack(images))
                        else:
                           images = np.expand_dims(np.array(np.vstack(images)), axis=-1)
                           p1s = np.expand_dims(np.vstack(p1s).flatten(),axis=-1)
                           p2s = np.expand_dims(np.vstack(p2s).flatten(),axis=-1)
                        yield images,[p1s, p2s]
                  else:
                     if len(images) >= batch_size:
                        yield np.array(images),[np.array(p1s), np.array(p2s)]
                  images, p1s, p2s = [], [], []

               elif len(vars)==3:
                  if len(CS)==0:
                      p1s = np.squeeze(np.array(p1s))
                      p2s = np.squeeze(np.array(p2s))
                      p3s = np.squeeze(np.array(p3s))
                  else:
                      p1s = np.squeeze(CS[0].transform(np.array(p1s).reshape(-1, 1)))
                      p2s = np.squeeze(CS[1].transform(np.array(p2s).reshape(-1, 1)))
                      p3s = np.squeeze(CS[2].transform(np.array(p3s).reshape(-1, 1)))
                  if do_aug==True:
                     if len(images) >= batch_size:
                        if greyscale==False:
                           images = np.array(np.vstack(images))
                        else:
                           images = np.expand_dims(np.array(np.vstack(images)), axis=-1)
                           p1s = np.expand_dims(np.vstack(p1s).flatten(),axis=-1)
                           p2s = np.expand_dims(np.vstack(p2s).flatten(),axis=-1)
                           p3s = np.expand_dims(np.vstack(p3s).flatten(),axis=-1)
                        yield images,[p1s, p2s, p3s]
                  else:
                     if len(images) >= batch_size:
                        yield np.array(images),[np.array(p1s), np.array(p2s), np.array(p3s)]
                  images, p1s, p2s, p3s = [], [], [], []

               elif len(vars)==4:
                  if len(CS)==0:
                      p1s = np.squeeze(np.array(p1s))
                      p2s = np.squeeze(np.array(p2s))
                      p3s = np.squeeze(np.array(p3s))
                      p4s = np.squeeze(np.array(p4s))
                  else:
                      p1s = np.squeeze(CS[0].transform(np.array(p1s).reshape(-1, 1)))
                      p2s = np.squeeze(CS[1].transform(np.array(p2s).reshape(-1, 1)))
                      p3s = np.squeeze(CS[2].transform(np.array(p3s).reshape(-1, 1)))
                      p4s = np.squeeze(CS[3].transform(np.array(p4s).reshape(-1, 1)))
                  if do_aug==True:
                     if len(images) >= batch_size:
                        if greyscale==False:
                           images = np.array(np.vstack(images))
                        else:
                           images = np.expand_dims(np.array(np.vstack(images)), axis=-1)
                           p1s = np.expand_dims(np.vstack(p1s).flatten(),axis=-1)
                           p2s = np.expand_dims(np.vstack(p2s).flatten(),axis=-1)
                           p3s = np.expand_dims(np.vstack(p3s).flatten(),axis=-1)
                           p4s = np.expand_dims(np.vstack(p4s).flatten(),axis=-1)
                        yield images,[p1s, p2s, p3s, p4s]
                  else:
                     if len(images) >= batch_size:
                        yield np.array(images),[np.array(p1s), np.array(p2s), np.array(p3s),
                              np.array(p4s)]
                  images, p1s, p2s, p3s, p4s = [], [], [], [], []

               elif len(vars)==5:
                  if len(CS)==0:
                      p1s = np.squeeze(np.array(p1s))
                      p2s = np.squeeze(np.array(p2s))
                      p3s = np.squeeze(np.array(p3s))
                      p4s = np.squeeze(np.array(p4s))
                      p5s = np.squeeze(np.array(p5s))
                  else:
                      p1s = np.squeeze(CS[0].transform(np.array(p1s).reshape(-1, 1)))
                      p2s = np.squeeze(CS[1].transform(np.array(p2s).reshape(-1, 1)))
                      p3s = np.squeeze(CS[2].transform(np.array(p3s).reshape(-1, 1)))
                      p4s = np.squeeze(CS[3].transform(np.array(p4s).reshape(-1, 1)))
                      p5s = np.squeeze(CS[4].transform(np.array(p5s).reshape(-1, 1)))
                  if do_aug==True:
                     if len(images) >= batch_size:
                        if greyscale==False:
                           images = np.array(np.vstack(images))
                        else:
                           images = np.expand_dims(np.array(np.vstack(images)), axis=-1)
                           p1s = np.expand_dims(np.vstack(p1s).flatten(),axis=-1)
                           p2s = np.expand_dims(np.vstack(p2s).flatten(),axis=-1)
                           p3s = np.expand_dims(np.vstack(p3s).flatten(),axis=-1)
                           p4s = np.expand_dims(np.vstack(p4s).flatten(),axis=-1)
                           p5s = np.expand_dims(np.vstack(p5s).flatten(),axis=-1)
                        yield images,[p1s, p2s, p3s, p4s, p5s]
                  else:
                     if len(images) >= batch_size:
                        yield np.array(images),[np.array(p1s), np.array(p2s), np.array(p3s),
                              np.array(p4s), np.array(p5s)]
                  images, p1s, p2s, p3s, p4s, p5s = [], [], [], [], [], []

               elif len(vars)==6:
                  if len(CS)==0:
                      p1s = np.squeeze(np.array(p1s))
                      p2s = np.squeeze(np.array(p2s))
                      p3s = np.squeeze(np.array(p3s))
                      p4s = np.squeeze(np.array(p4s))
                      p5s = np.squeeze(np.array(p5s))
                      p6s = np.squeeze(np.array(p6s))
                  else:
                      p1s = np.squeeze(CS[0].transform(np.array(p1s).reshape(-1, 1)))
                      p2s = np.squeeze(CS[1].transform(np.array(p2s).reshape(-1, 1)))
                      p3s = np.squeeze(CS[2].transform(np.array(p3s).reshape(-1, 1)))
                      p4s = np.squeeze(CS[3].transform(np.array(p4s).reshape(-1, 1)))
                      p5s = np.squeeze(CS[4].transform(np.array(p5s).reshape(-1, 1)))
                      p6s = np.squeeze(CS[5].transform(np.array(p6s).reshape(-1, 1)))
                  if do_aug==True:
                     if len(images) >= batch_size:
                        if greyscale==False:
                           images = np.array(np.vstack(images))
                        else:
                           images = np.expand_dims(np.array(np.vstack(images)), axis=-1)
                           p1s = np.expand_dims(np.vstack(p1s).flatten(),axis=-1)
                           p2s = np.expand_dims(np.vstack(p2s).flatten(),axis=-1)
                           p3s = np.expand_dims(np.vstack(p3s).flatten(),axis=-1)
                           p4s = np.expand_dims(np.vstack(p4s).flatten(),axis=-1)
                           p5s = np.expand_dims(np.vstack(p5s).flatten(),axis=-1)
                           p6s = np.expand_dims(np.vstack(p6s).flatten(),axis=-1)
                        yield images,[p1s, p2s, p3s, p4s, p5s, p6s]
                  else:
                     if len(images) >= batch_size:
                        yield np.array(images),[np.array(p1s), np.array(p2s), np.array(p3s),
                              np.array(p4s), np.array(p5s), np.array(p6s)]
                  images, p1s, p2s, p3s, p4s, p5s, p6s = \
                  [], [], [], [], [], [], []

               elif len(vars)==7:
                  if len(CS)==0:
                      p1s = np.squeeze(np.array(p1s))
                      p2s = np.squeeze(np.array(p2s))
                      p3s = np.squeeze(np.array(p3s))
                      p4s = np.squeeze(np.array(p4s))
                      p5s = np.squeeze(np.array(p5s))
                      p6s = np.squeeze(np.array(p6s))
                      p7s = np.squeeze(np.array(p7s))
                  else:
                      p1s = np.squeeze(CS[0].transform(np.array(p1s).reshape(-1, 1)))
                      p2s = np.squeeze(CS[1].transform(np.array(p2s).reshape(-1, 1)))
                      p3s = np.squeeze(CS[2].transform(np.array(p3s).reshape(-1, 1)))
                      p4s = np.squeeze(CS[3].transform(np.array(p4s).reshape(-1, 1)))
                      p5s = np.squeeze(CS[4].transform(np.array(p5s).reshape(-1, 1)))
                      p6s = np.squeeze(CS[5].transform(np.array(p6s).reshape(-1, 1)))
                      p7s = np.squeeze(CS[6].transform(np.array(p7s).reshape(-1, 1)))
                  if do_aug==True:
                     if len(images) >= batch_size:
                        if greyscale==False:
                           images = np.array(np.vstack(images))
                        else:
                           images = np.expand_dims(np.array(np.vstack(images)), axis=-1)
                           p1s = np.expand_dims(np.vstack(p1s).flatten(),axis=-1)
                           p2s = np.expand_dims(np.vstack(p2s).flatten(),axis=-1)
                           p3s = np.expand_dims(np.vstack(p3s).flatten(),axis=-1)
                           p4s = np.expand_dims(np.vstack(p4s).flatten(),axis=-1)
                           p5s = np.expand_dims(np.vstack(p5s).flatten(),axis=-1)
                           p6s = np.expand_dims(np.vstack(p6s).flatten(),axis=-1)
                           p7s = np.expand_dims(np.vstack(p7s).flatten(),axis=-1)
                        yield images,[p1s, p2s, p3s, p4s, p5s, p6s, p7s]
                  else:
                     if len(images) >= batch_size:
                        yield np.array(images),[np.array(p1s), np.array(p2s), np.array(p3s),
                              np.array(p4s), np.array(p5s), np.array(p6s),
                              np.array(p7s)]
                  images, p1s, p2s, p3s, p4s, p5s, p6s, p7s = \
                  [], [], [], [], [], [], [], []

               elif len(vars)==8:
                  if len(CS)==0:
                      p1s = np.squeeze(np.array(p1s))
                      p2s = np.squeeze(np.array(p2s))
                      p3s = np.squeeze(np.array(p3s))
                      p4s = np.squeeze(np.array(p4s))
                      p5s = np.squeeze(np.array(p5s))
                      p6s = np.squeeze(np.array(p6s))
                      p7s = np.squeeze(np.array(p7s))
                      p8s = np.squeeze(np.array(p8s))
                  else:
                      p1s = np.squeeze(CS[0].transform(np.array(p1s).reshape(-1, 1)))
                      p2s = np.squeeze(CS[1].transform(np.array(p2s).reshape(-1, 1)))
                      p3s = np.squeeze(CS[2].transform(np.array(p3s).reshape(-1, 1)))
                      p4s = np.squeeze(CS[3].transform(np.array(p4s).reshape(-1, 1)))
                      p5s = np.squeeze(CS[4].transform(np.array(p5s).reshape(-1, 1)))
                      p6s = np.squeeze(CS[5].transform(np.array(p6s).reshape(-1, 1)))
                      p7s = np.squeeze(CS[6].transform(np.array(p7s).reshape(-1, 1)))
                      p8s = np.squeeze(CS[7].transform(np.array(p8s).reshape(-1, 1)))
                  if do_aug==True:
                     if len(images) >= batch_size:
                        if greyscale==False:
                           images = np.array(np.vstack(images))
                        else:
                           images = np.expand_dims(np.array(np.vstack(images)), axis=-1)
                           p1s = np.expand_dims(np.vstack(p1s).flatten(),axis=-1)
                           p2s = np.expand_dims(np.vstack(p2s).flatten(),axis=-1)
                           p3s = np.expand_dims(np.vstack(p3s).flatten(),axis=-1)
                           p4s = np.expand_dims(np.vstack(p4s).flatten(),axis=-1)
                           p5s = np.expand_dims(np.vstack(p5s).flatten(),axis=-1)
                           p6s = np.expand_dims(np.vstack(p6s).flatten(),axis=-1)
                           p7s = np.expand_dims(np.vstack(p7s).flatten(),axis=-1)
                           p8s = np.expand_dims(np.vstack(p8s).flatten(),axis=-1)
                        yield images,[p1s, p2s, p3s, p4s, p5s, p6s, p7s, p8s]

                  else:
                     if len(images) >= batch_size:
                        yield np.array(images),[np.array(p1s), np.array(p2s), np.array(p3s),
                              np.array(p4s), np.array(p5s), np.array(p6s),
                              np.array(p7s), np.array(p8s)]
                  images, p1s, p2s, p3s, p4s, p5s, p6s, p7s, p8s = \
                  [], [], [], [], [], [], [], [], []

               elif len(vars)==9:
                  if len(CS)==0:
                      p1s = np.squeeze(np.array(p1s))
                      p2s = np.squeeze(np.array(p2s))
                      p3s = np.squeeze(np.array(p3s))
                      p4s = np.squeeze(np.array(p4s))
                      p5s = np.squeeze(np.array(p5s))
                      p6s = np.squeeze(np.array(p6s))
                      p7s = np.squeeze(np.array(p7s))
                      p8s = np.squeeze(np.array(p8s))
                      p9s = np.squeeze(np.array(p9s))
                  else:
                      p1s = np.squeeze(CS[0].transform(np.array(p1s).reshape(-1, 1)))
                      p2s = np.squeeze(CS[1].transform(np.array(p2s).reshape(-1, 1)))
                      p3s = np.squeeze(CS[2].transform(np.array(p3s).reshape(-1, 1)))
                      p4s = np.squeeze(CS[3].transform(np.array(p4s).reshape(-1, 1)))
                      p5s = np.squeeze(CS[4].transform(np.array(p5s).reshape(-1, 1)))
                      p6s = np.squeeze(CS[5].transform(np.array(p6s).reshape(-1, 1)))
                      p7s = np.squeeze(CS[6].transform(np.array(p7s).reshape(-1, 1)))
                      p8s = np.squeeze(CS[7].transform(np.array(p8s).reshape(-1, 1)))
                      p9s = np.squeeze(CS[8].transform(np.array(p9s).reshape(-1, 1)))

                  try:
                     if do_aug==True:
                         if len(images) >= batch_size:
                            if greyscale==False:
                               images = np.array(np.vstack(images))
                            else:
                               images = np.expand_dims(np.array(np.vstack(images)), axis=-1)
                               p1s = np.expand_dims(np.vstack(p1s).flatten(),axis=-1)
                               p2s = np.expand_dims(np.vstack(p2s).flatten(),axis=-1)
                               p3s = np.expand_dims(np.vstack(p3s).flatten(),axis=-1)
                               p4s = np.expand_dims(np.vstack(p4s).flatten(),axis=-1)
                               p5s = np.expand_dims(np.vstack(p5s).flatten(),axis=-1)
                               p6s = np.expand_dims(np.vstack(p6s).flatten(),axis=-1)
                               p7s = np.expand_dims(np.vstack(p7s).flatten(),axis=-1)
                               p8s = np.expand_dims(np.vstack(p8s).flatten(),axis=-1)
                               p9s = np.expand_dims(np.vstack(p9s).flatten(),axis=-1)
                            yield images,[p1s, p2s, p3s, p4s, p5s, p6s, p7s, p8s, p9s]
                     else:
                         if len(images) >= batch_size:
                            yield np.array(images),[np.array(p1s), np.array(p2s), np.array(p3s),
                                  np.array(p4s), np.array(p5s), np.array(p6s),
                                  np.array(p7s), np.array(p8s), np.array(p9s)]
                  except GeneratorExit:
                      print(" ")
                  images, p1s, p2s, p3s, p4s, p5s, p6s, p7s, p8s, p9s = \
                  [], [], [], [], [], [], [], [], [], []

        if not for_training:
            break


###===================================================
def get_data_generator_1image(df, indices, for_training, ID_MAP,
                              var, batch_size, greyscale, do_aug):
    """
    This function creates a dataset generator consisting of batches of images
    and corresponding one-hot-encoded labels describing the sediment in each image
    """
    try:
        ID_MAP2 = dict((g, i) for i, g in ID_MAP.items())
    except:
        ID_MAP = dict(zip(np.arange(ID_MAP), [str(k) for k in range(ID_MAP)]))
        ID_MAP2 = dict((g, i) for i, g in ID_MAP.items())

    images, pops = [], []
    while True:
        for i in indices:
            r = df.iloc[i]
            file, pop = r['files'], r[var]

            if greyscale==True:
               im = Image.open(file).convert('LA')
               if np.ndim(im)==3:
                   im = im[:,:,0]
               im = im.resize((IM_HEIGHT, IM_HEIGHT))
               im = np.array(im)[:,:,0]
            else:
               im = Image.open(file)
               if np.ndim(im)==2:
                  im = np.array(im)
                  im = np.dstack((im, im , im))
                  im = Image.fromarray(im)

            im = im.resize((IM_HEIGHT, IM_HEIGHT))
            im = np.array(im) / 255.0

            if greyscale==False:
                if np.ndim(im)==3:
                    pass
            else:
                if np.ndim(im)==2:
                    pass

            if greyscale==True:
               if do_aug==True:
                   aug = apply_aug(im[:,:,0])
                   images.append(aug)
                   pops.append([to_categorical(pop, len(ID_MAP2)) for k in range(2)]) #3
               else:
                   images.append(np.expand_dims(im[:,:,0], axis=2))
            else:
               if do_aug==True:
                   aug = apply_aug(im)
                   images.append(aug)
                   pops.append([to_categorical(pop, len(ID_MAP2)) for k in range(2)])
               else:
                   images.append(im)
                   pops.append(to_categorical(pop, len(ID_MAP2)))

            try:

               if do_aug==True:
                  if len(images) >= batch_size:
                     if greyscale==False:
                        images = np.array(np.vstack(images))
                        pops = np.array(np.vstack(pops))
                     else:
                        images = np.expand_dims(np.array(np.vstack(images)), axis=-1)
                        pops = np.array(np.vstack(pops))
                     yield images, pops
                     images, pops = [], []
               else:
                  if len(images) >= batch_size:
                     yield np.squeeze(np.array(images)),np.array(pops) #[np.array(pops)]
                     images, pops = [], []

            except GeneratorExit:
               print(" ") #pass

        if not for_training:
            break


###===================================================
### PLOT TRAINING HISTORY FUNCTIONS

def  plot_train_history_1var(history):
   """
   This function plots loss and accuracy curves from the model training
   """
   fig, axes = plt.subplots(1, 2, figsize=(10, 10))

   print(history.history.keys())

   axes[0].plot(history.history['loss'], label='Training loss')
   axes[0].plot(history.history['val_loss'], label='Validation loss')
   axes[0].set_xlabel('Epochs')
   axes[0].legend()
   try:
      axes[1].plot(history.history['acc'], label='pop train accuracy')
      axes[1].plot(history.history['val_acc'], label='pop test accuracy')
   except:
      axes[1].plot(history.history['accuracy'], label='pop train accuracy')
      axes[1].plot(history.history['val_accuracy'], label='pop test accuracy')
   axes[1].set_xlabel('Epochs')
   axes[1].legend()


###===================================================
def plot_train_history_Nvar(history, varuse, N):
    """
    This function makes a plot of error train/validation history for 9 variables,
    plus overall loss functions
    """
    fig, axes = plt.subplots(1, N+1, figsize=(20, 5))
    for k in range(N):
       try:
          axes[k].plot(history.history[varuse[k]+'_output_mean_absolute_error'],
                       label=varuse[k]+' Train MAE')
          axes[k].plot(history.history['val_'+varuse[k]+'_output_mean_absolute_error'],
                       label=varuse[k]+' Val MAE')
       except:
          axes[k].plot(history.history[varuse[k]+'_output_mae'],
                       label=varuse[k]+' Train MAE')
          axes[k].plot(history.history['val_'+varuse[k]+'_output_mae'],
                       label=varuse[k]+' Val MAE')
       axes[k].set_xlabel('Epochs')
       axes[k].legend()

    axes[N].plot(history.history['loss'], label='Training loss')
    axes[N].plot(history.history['val_loss'], label='Validation loss')
    axes[N].set_xlabel('Epochs')
    axes[N].legend()


###===================================================
def  plot_train_history_1var_mae(history):
   """
   This function plots loss and accuracy curves from the model training
   """
   print(history.history.keys())

   fig, axes = plt.subplots(1, 2, figsize=(10, 10))

   axes[0].plot(history.history['loss'], label='Training loss')
   axes[0].plot(history.history['val_loss'],
                label='Validation loss')
   axes[0].set_xlabel('Epochs')
   axes[0].legend()

   try:
      axes[1].plot(history.history['mean_absolute_error'],
                   label='pop train MAE')
      axes[1].plot(history.history['val_mean_absolute_error'],
                   label='pop test MAE')
   except:
      axes[1].plot(history.history['mae'], label='pop train MAE')
      axes[1].plot(history.history['val_mae'], label='pop test MAE')

   axes[1].set_xlabel('Epochs')
   axes[1].legend()

###===================================================
### PLOT CONFUSION MATRIX FUNCTIONS

###===================================================
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          cmap=plt.cm.Purples,
                          dolabels=True):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        cm[np.isnan(cm)] = 0

    plt.imshow(cm, interpolation='nearest', cmap=cmap, vmax=1, vmin=0)
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    if dolabels==True:
       tick_marks = np.arange(len(classes))
       plt.xticks(tick_marks, classes, fontsize=3) #, rotation=60
       plt.yticks(tick_marks, classes, fontsize=3)

       plt.ylabel('True label',fontsize=4)
       plt.xlabel('Estimated label',fontsize=4)

    else:
       plt.axis('off')

    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if cm[i, j]>0:
           plt.text(j, i, str(cm[i, j])[:4],fontsize=5,
                    horizontalalignment="center",
                    color="white" if cm[i, j] > 0.6 else "black")
    #plt.tight_layout()

    plt.xlim(-0.5, len(classes))
    plt.ylim(-0.5, len(classes))
    return cm

###===================================================
def plot_confmat(y_pred, y_true, prefix, classes):
   """
   This function generates and plots a confusion matrix
   """
   base = prefix+'_'

   y = y_pred.copy()
   del y_pred
   l = y_true.copy()
   del y_true

   l = l.astype('float')
   ytrue = l.flatten()
   ypred = y.flatten()

   ytrue = ytrue[~np.isnan(ytrue)]
   ypred = ypred[~np.isnan(ypred)]

   cm = confusion_matrix(ytrue, ypred)
   cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
   cm[np.isnan(cm)] = 0

   fig=plt.figure()
   plt.subplot(221)
   plot_confusion_matrix(cm, classes=classes)



###===================================================
### PREDICTION FUNCTIONS

def predict_test_train_cat(train_df, test_df, train_idx, test_idx, var, SM,
                           classes, weights_path, greyscale, name, do_aug):
   """
   This function creates makes predictions on test and train data,
   prints a classification report, and prints confusion matrices
   """
   # if type(SM) == list:
   #    counter = 0
   #    for s,wp in zip(SM, weights_path):
   #       exec('SM[counter].load_weights(wp)')
   #    counter += 1
   # else:
   #   SM.load_weights(weights_path)

   ##==============================================
   ## make predictions on training data
   train_gen = get_data_generator_1image(train_df, train_idx, False,
               len(classes), var, np.min((1000, len(train_idx))), greyscale, do_aug)
   x_train, (trueT)= next(train_gen)

   PT = []

   if type(SM) == list:
       #counter = 0
       for s in SM:
           tmp=s.predict(x_train, batch_size=8)
           exec(
              'PT.append(np.asarray(np.squeeze(tmp)))'
           )
           del tmp

       predT = np.median(PT, axis=0)
       del PT
       K.clear_session()
       gc.collect()

   else:
     predT = SM.predict(x_train, batch_size=8)

   del train_gen, x_train

   if test_df is not None:
       ## make predictions on testing data
       test_gen = get_data_generator_1image(test_df, test_idx, False,
                  len(classes), var, np.min((1000, len(test_idx))), greyscale, False) #no augmentation on validation data
       x_test, (true)= next(test_gen)

       PT = []

       if type(SM) == list:
           #counter = 0
           for s in SM:
               tmp=s.predict(x_test, batch_size=8)
               exec(
                  'PT.append(np.asarray(np.squeeze(tmp)))'
               )
               del tmp

           pred = np.median(PT, axis=0)
           del PT
           K.clear_session()
           gc.collect()

       else:

           pred = SM.predict(x_test, batch_size=8) #1)

       del test_gen, x_test

   trueT = np.squeeze(np.asarray(trueT).argmax(axis=-1) )
   predT = np.squeeze(np.asarray(predT).argmax(axis=-1))#[0])

   if test_df is not None:
       pred = np.squeeze(np.asarray(pred).argmax(axis=-1))#[0])
       true = np.squeeze(np.asarray(true).argmax(axis=-1) )

       ##==============================================
       ## print a classification report to screen, showing f1, precision, recall and accuracy
       print("==========================================")
       print("Classification report for "+var)
       print(classification_report(true, pred))

   fig = plt.figure()
   ##==============================================
   ## create figures showing confusion matrices for train and test data sets
   if type(SM) == list:
      if test_df is not None:
          plot_confmat(pred, true, var, classes)
          plt.savefig(weights_path[0].replace('.hdf5','_cm.png').\
                   replace('batch','_'.join(np.asarray(BATCH_SIZE, dtype='str'))),
                   dpi=300, bbox_inches='tight')
          plt.close('all')

      plot_confmat(predT, trueT, var+'T',classes)
      plt.savefig(weights_path[0].replace('.hdf5','_cmT.png').\
               replace('batch','_'.join(np.asarray(BATCH_SIZE, dtype='str'))),
               dpi=300, bbox_inches='tight')
      plt.close('all')

   else:
      if test_df is not None:
          plot_confmat(pred, true, var, classes)
          plt.savefig(weights_path.replace('.hdf5','_cm.png'),
                   dpi=300, bbox_inches='tight')
          plt.close('all')

      plot_confmat(predT, trueT, var+'T',classes)
      plt.savefig(weights_path.replace('.hdf5','_cmT.png'),
               dpi=300, bbox_inches='tight')
      plt.close('all')

   plt.close()
   del fig

###===================================================
def predict_test_train_siso_simo(train_df, test_df, train_idx, test_idx, vars,
                                 SM, weights_path, name, mode, greyscale,
                                 CS, dropout, scale, do_aug):
    """
    This function creates makes predcitions on test and train data
    """
    ##==============================================
    ## make predictions on training data
    if type(SM) == list:
        counter = 0
        for s,wp in zip(SM, weights_path):
           exec('SM[counter].load_weights(wp)')
        counter += 1
    else:
        SM.load_weights(weights_path)


    train_gen = get_data_generator_Nvars_siso_simo(train_df, train_idx, False,
                vars, np.min((400, len(train_idx))), greyscale, CS, False) #
    x_train, tmp = next(train_gen)

    if scale == True:

        if len(vars)>1:
           counter = 0
           for v in vars:
              exec(
              v+\
              '_trueT = np.squeeze(CS[counter].inverse_transform(tmp[counter].reshape(-1,1)))'
              )
              counter +=1
        else:
           exec(
           vars[0]+\
           '_trueT = np.squeeze(CS[0].inverse_transform(tmp[0].reshape(-1,1)))'
           )

    else:
        if len(vars)>1:
           counter = 0
           for v in vars:
              exec(
              v+\
              '_trueT = np.squeeze(tmp[counter])'
              )
              counter +=1
        else:
           exec(
           vars[0]+\
           '_trueT = np.squeeze(tmp)'
           )

    del tmp

    for v in vars:
       exec(v+'_PT = []')

    if scale == True:

        if type(SM) == list:
            counter = 0 #model iterator
            for s in SM:
                tmp=s.predict(x_train, batch_size=8)

                if len(vars)>1:
                   counter2 = 0 #variable iterator
                   for v in vars:
                      exec(
                      v+\
                      '_PT.append(np.squeeze(CS[counter].inverse_transform(tmp[counter2].reshape(-1,1))))'
                      )
                      counter2 +=1
                else:
                   exec(
                   vars[0]+\
                   '_PT.append(np.asarray(np.squeeze(CS[0].inverse_transform(tmp.reshape(-1,1)))))'
                   )

                del tmp

            if len(vars)>1:
               for v in vars:
                  exec(
                  v+\
                  '_PT = np.median('+v+'_PT, axis=0)'
                  )
            else:
               exec(
               vars[0]+\
               '_PT = np.median('+v+'_PT, axis=0)'
               )

        else:
            tmp = SM.predict(x_train, batch_size=8) #128)

            if len(vars)>1:
               counter = 0
               for v in vars:
                  exec(
                  v+\
                  '_PT.append(np.squeeze(CS[counter].inverse_transform(tmp[counter].reshape(-1,1))))'
                  )
                  counter +=1
            else:
               exec(
               vars[0]+\
               '_PT.append(np.asarray(np.squeeze(CS[0].inverse_transform(tmp.reshape(-1,1)))))'
               )

            del tmp

    else:

        if type(SM) == list:
            for s in SM:
                tmp=s.predict(x_train, batch_size=8)

                if len(vars)>1:
                   counter2 = 0
                   for v in vars:
                      exec(
                      v+\
                      '_PT.append(np.squeeze(tmp[counter2]))'
                      )
                      counter2 +=1
                else:
                   exec(
                   vars[0]+\
                   '_PT.append(np.asarray(tmp))'
                   )

                del tmp

            if len(vars)>1:
               for v in vars:
                  exec(
                  v+\
                  '_PT = np.median('+v+'_PT, axis=0)'
                  )
            else:
               exec(
               vars[0]+\
               '_PT = np.median('+v+'_PT, axis=0)'
               )

        else:
            tmp = SM.predict(x_train, batch_size=8) #128)

            if len(vars)>1:
               counter = 0
               for v in vars:
                  exec(
                  v+\
                  '_PT.append(np.squeeze(tmp[counter]))'
                  )
                  counter +=1
            else:
               exec(
               vars[0]+\
               '_PT.append(np.asarray(np.squeeze(tmp)))'
               )

            del tmp



    if len(vars)>1:
       for k in range(len(vars)):
          exec(vars[k]+'_predT = np.squeeze(np.asarray('+vars[k]+'_PT))')
    else:
       exec(vars[0]+'_predT = np.squeeze(np.asarray('+vars[0]+'_PT))')


    for v in vars:
       exec('del '+v+'_PT')


    del train_gen, x_train

    ## make predictions on testing data
    if test_df is not None:
        test_gen = get_data_generator_Nvars_siso_simo(test_df, test_idx, False,
                   vars, np.min((400, len(test_idx))), greyscale, CS, False) #

        x_test, tmp = next(test_gen)

        if scale == True:

            if len(vars)>1:
               counter = 0
               for v in vars:
                  exec(
                  v+\
                  '_true = np.squeeze(CS[counter].inverse_transform(tmp[counter].reshape(-1,1)))'
                  )
                  counter +=1
            else:
               exec(
               vars[0]+\
               '_true = np.squeeze(CS[0].inverse_transform(tmp[0].reshape(-1,1)))'
               )

        else:
            if len(vars)>1:
               counter = 0
               for v in vars:
                  exec(
                  v+\
                  '_true = np.squeeze(tmp[counter])'
                  )
                  counter +=1
            else:
               exec(
               vars[0]+\
               '_true = np.squeeze(tmp)'
               )


        del tmp

        for v in vars:
           exec(v+'_P = []')

        if scale == True:

            if type(SM) == list:
                #counter = 0
                for s in SM:
                    tmp=s.predict(x_test, batch_size=8)

                    if len(vars)>1:
                       counter = 0
                       for v in vars:
                          exec(
                          v+\
                          '_P.append(np.squeeze(CS[counter].inverse_transform(tmp[counter].reshape(-1,1))))'
                          )
                          counter +=1
                    else:
                       exec(
                       vars[0]+\
                       '_P.append(np.asarray(np.squeeze(CS[0].inverse_transform(tmp.reshape(-1,1)))))'
                       )

                    del tmp

                if len(vars)>1:
                   for v in vars:
                      exec(
                      v+\
                      '_P = np.median('+v+'_P, axis=0)'
                      )
                else:
                   exec(
                   vars[0]+\
                   '_P = np.median('+v+'_P, axis=0)'
                   )

            else:

                tmp = SM.predict(x_test, batch_size=8) #128)
                if len(vars)>1:
                   counter = 0
                   for v in vars:
                      exec(
                      v+\
                      '_P.append(np.squeeze(CS[counter].inverse_transform(tmp[counter].reshape(-1,1))))'
                      )
                      counter +=1
                else:
                   exec(
                   vars[0]+\
                   '_P.append(np.asarray(np.squeeze(CS[0].inverse_transform(tmp.reshape(-1,1)))))'
                   )

                del tmp


        else:
            if type(SM) == list:
                counter = 0
                for s in SM:
                    tmp=s.predict(x_test, batch_size=8)

                    if len(vars)>1:
                       counter = 0
                       for v in vars:
                          exec(
                          v+\
                          '_P.append(np.squeeze(tmp[counter]))'
                          )
                          counter +=1
                    else:
                       exec(
                       vars[0]+\
                       '_P.append(np.asarray(np.squeeze(tmp)))'
                       )

                    del tmp

                if len(vars)>1:
                   for v in vars:
                      exec(
                      v+\
                      '_P = np.median('+v+'_P, axis=0)'
                      )
                else:
                   exec(
                   vars[0]+\
                   '_P = np.median('+v+'_P, axis=0)'
                   )

            else:

                tmp = SM.predict(x_test, batch_size=8) #128)
                if len(vars)>1:
                   counter = 0
                   for v in vars:
                      exec(
                      v+\
                      '_P.append(np.squeeze(tmp[counter]))'
                      )
                      counter +=1
                else:
                   exec(
                   vars[0]+\
                   '_P.append(np.asarray(np.squeeze(tmp)))'
                   )

                del tmp


        del test_gen, x_test

        if len(vars)>1:
           for k in range(len(vars)):
              exec(vars[k]+'_pred = np.squeeze(np.asarray('+vars[k]+'_P))')
        else:
           exec(vars[0]+'_pred = np.squeeze(np.asarray('+vars[0]+'_P))')

        for v in vars:
           exec('del '+v+'_P')

        # ## write out results to text files
        # if len(vars)>1:
        #    for k in range(len(vars)):
        #       exec('np.savetxt("'+name+'_test'+vars[k]+'_pred.txt", ('+vars[k]+'_pred))')
        #       exec('np.savetxt("'+name+'_train'+vars[k]+'_predT.txt", ('+vars[k]+'_predT))')
        #       exec('np.savetxt("'+name+'_test'+vars[k]+'_true.txt", ('+vars[k]+'_true))')
        #       exec('np.savetxt("'+name+'_train'+vars[k]+'_trueT.txt", ('+vars[k]+'_trueT))')
        #    np.savetxt(name+"_test_files.txt", np.asarray(test_df.files.values), fmt="%s")
        #    np.savetxt(name+"_train_files.txt", np.asarray(train_df.files.values), fmt="%s")
        #
        # else:
        #    exec('np.savetxt("'+name+'_test'+vars[0]+'.txt", ('+vars[0]+'_pred))')
        #    exec('np.savetxt("'+name+'_train'+vars[0]+'.txt", ('+vars[0]+'_predT))')
        #    exec('np.savetxt("'+name+'_test'+vars[0]+'_true.txt", ('+vars[0]+'_true))')
        #    exec('np.savetxt("'+name+'_train'+vars[0]+'_trueT.txt", ('+vars[0]+'_trueT))')
        #    np.savetxt(name+"_test_files.txt", np.asarray(test_df.files.values), fmt="%s")
        #    np.savetxt(name+"_train_files.txt", np.asarray(train_df.files.values), fmt="%s")



    if len(vars)==9:
       nrows = 3; ncols = 3
    elif len(vars)==8:
       nrows = 2; ncols = 4
    elif len(vars)==7:
       nrows = 3; ncols = 3
    elif len(vars)==6:
       nrows = 3; ncols = 2
    elif len(vars)==5:
       nrows = 3; ncols = 2
    elif len(vars)==4:
       nrows = 2; ncols = 2
    elif len(vars)==3:
       nrows = 2; ncols = 2
    elif len(vars)==2:
       nrows = 1; ncols = 2
    elif len(vars)==1:
       nrows = 1; ncols = 1

    Z = []

    ## make a plot
    fig = plt.figure(figsize=(6*nrows,4*ncols))
    labs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for k in range(1,1+(nrows*ncols)):
      try:
         plt.subplot(nrows,ncols,k)
         x1 = eval(vars[k-1]+'_trueT')
         y1 = eval(vars[k-1]+'_predT')

         z = np.polyfit(y1,x1, 1)
         Z.append(z)

         y1 = np.polyval(z,y1)
         y1 = np.abs(y1)

         # if k==4: #for k in range(len(vars)):
         #    ind = np.where(100*np.abs(x1-y1)/x1)[0] < 50
         #    exec('np.savetxt("'+name+'_train'+vars[k]+'_predT.txt", (y1[ind]))')
         #    exec('np.savetxt("'+name+'_train'+vars[k]+'_trueT.txt", (x1[ind]))')
         #    np.savetxt(name+"_train_files"+vars[k]+"_.txt", np.asarray(train_df.files.values)[ind], fmt="%s")

         plt.plot(x1, y1, 'ko', markersize=5)
         plt.plot([ np.min(np.hstack((x1,y1))),  np.max(np.hstack((x1,y1)))],
                  [ np.min(np.hstack((x1,y1))),  np.max(np.hstack((x1,y1)))],
                  'k', lw=2)

         if test_df is not None:
             x2 = eval(vars[k-1]+'_true')
             y2 = eval(vars[k-1]+'_pred')
             y2 = np.abs(np.polyval(z,y2))

             # if k==4: #for k in range(len(vars)):
             #    ind = np.where(100*np.abs(x2-y2)/x2)[0] < 50
             #    exec('np.savetxt("'+name+'_test'+vars[k]+'_pred.txt", (y2[ind]))')
             #    exec('np.savetxt("'+name+'_test'+vars[k]+'_true.txt", (x2[ind]))')
             #    np.savetxt(name+"_test_files"+vars[k]+"_.txt", np.asarray(train_df.files.values)[ind], fmt="%s")

             plt.plot(x2, y2, 'bx', markersize=5)

         if test_df is not None:
             plt.text(np.nanmin(x2), 0.75*np.max(np.hstack((x2,y2))),'Test : '+\
                      str(np.mean(100*(np.abs(y2-x2) / x2)))[:5]+\
                      ' %',  fontsize=10, color='b')
             plt.text(np.nanmin(x1), 0.7*np.max(np.hstack((x1,y1))),'Train : '+\
                      str(np.mean(100*(np.abs(y1-x1) / x1)))[:5]+\
                      ' %', fontsize=10)
         else:
             plt.text(np.nanmin(x1), 0.7*np.max(np.hstack((x1,y1))),''+\
                      str(np.mean(100*(np.abs(y1-x1) / x1)))[:5]+\
                      ' %', fontsize=10)
         plt.title(r''+labs[k-1]+') '+vars[k-1], fontsize=8, loc='left')

         #varstring = ''.join([str(k)+'_' for k in vars])
         varstring = str(len(vars))+'vars'

      except:
          pass
    if type(SM) == list:
       plt.savefig(weights_path[0].replace('.hdf5', '_skill_ensemble.png').\
                replace('batch','_'.join(np.asarray(BATCH_SIZE, dtype='str'))),
                dpi=300, bbox_inches='tight')
       joblib.dump(Z, weights_path[0].replace('.hdf5','_bias.pkl').\
                replace('batch','_'.join(np.asarray(BATCH_SIZE, dtype='str'))))

    else:
       plt.savefig(weights_path.replace('.hdf5', '_skill.png'),
                dpi=300, bbox_inches='tight')
       joblib.dump(Z, weights_path.replace('.hdf5','_bias.pkl'))

    plt.close()
    del fig






###===================================================
### MISC. UTILITIES

def tidy(name,res_folder):
    """
    This function moves training outputs to a specific folder
    """

    pngfiles = glob('*'+name+'*.png')
    jsonfiles = glob('*'+name+'*.json')
    hfiles = glob('*'+name+'*.hdf5')
    tfiles = glob('*'+name+'*.txt')
    pfiles = glob('*'+name+'*.pkl')

    try:
       [shutil.move(k, res_folder) for k in pngfiles]
       [shutil.move(k, res_folder) for k in hfiles]
       [shutil.move(k, res_folder) for k in jsonfiles]
       [shutil.move(k, res_folder) for k in tfiles]
       [shutil.move(k, res_folder) for k in pfiles]
    except:
       pass

###===================================================
def get_df(csvfile):
    """
    This function reads a csvfile with image names and labels
    and returns random indices
    """
    ###===================================================
    ## read the data set in, clean and modify the pathnames so they are absolute
    df = pd.read_csv(csvfile)

    df['files'] = [k.strip() for k in df['files']]

    df['files'] = [os.getcwd()+os.sep+f.replace('\\',os.sep) for f in df['files']]

    np.random.seed(2019)
    return np.random.permutation(len(df)), df



#
# ###===================================================
# def predict_test_train_miso_mimo(train_df, test_df, train_idx, test_idx,
#                                  vars, auxin, SM, weights_path, name, mode,
#                                  greyscale, CS, CSaux):
#     """
#     This function creates makes predcitions on test and train data
#     """
#     ##==============================================
#     ## make predictions on training data
#
#     SM.load_weights(weights_path)
#
#     train_gen = get_data_generator_Nvars_miso_mimo(train_df, train_idx, False,
#                  vars, auxin,aux_mean, aux_std, len(train_idx), greyscale)
#
#     x_train, tmp = next(train_gen)
#
#     if len(vars)>1:
#        counter = 0
#        for v in vars:
#           exec(
#           v+\
#           '_trueT = np.squeeze(CS[counter].inverse_transform(tmp[counter].reshape(-1,1)))'
#           )
#           counter +=1
#     else:
#        exec(
#        vars[0]+\
#        '_trueT = np.squeeze(CS[0].inverse_transform(tmp[0].reshape(-1,1)))'
#        )
#
#     for v in vars:
#        exec(v+'_PT = []')
#
#     del tmp
#     tmp = SM.predict(x_train, batch_size=8) #128)
#     if len(vars)>1:
#        counter = 0
#        for v in vars:
#           exec(
#               v+\
#               '_PT.append(np.squeeze(CS[counter].inverse_transform(tmp[counter].reshape(-1,1))))'
#               )
#           counter +=1
#     else:
#        exec(
#        vars[0]+\
#        '_PT.append(np.asarray(np.squeeze(CS[0].inverse_transform(tmp.reshape(-1,1)))))'
#        )
#
#
#     if len(vars)>1:
#        for k in range(len(vars)):
#           exec(
#           vars[k]+\
#           '_predT = np.squeeze(np.mean(np.asarray('+vars[k]+'_PT), axis=0))'
#           )
#     else:
#        exec(
#        vars[0]+\
#        '_predT = np.squeeze(np.mean(np.asarray('+vars[0]+'_PT), axis=0))'
#        )
#
#     ## make predictions on testing data
#     test_gen = get_data_generator_Nvars_miso_mimo(test_df, test_idx, False,
#                  vars, auxin, aux_mean, aux_std, len(test_idx), greyscale)
#
#     del tmp
#     x_test, tmp = next(test_gen)
#     if len(vars)>1:
#        counter = 0
#        for v in vars:
#           exec(v+\
#                '_true = np.squeeze(CS[counter].inverse_transform(tmp[counter].reshape(-1,1)))'
#                )
#           counter +=1
#     else:
#        exec(vars[0]+\
#        '_true = np.squeeze(CS[0].inverse_transform(tmp[0].reshape(-1,1)))'
#        )
#
#     for v in vars:
#        exec(v+'_P = []')
#
#     del tmp
#     tmp = SM.predict(x_test, batch_size=8) #128)
#     if len(vars)>1:
#        counter = 0
#        for v in vars:
#           exec(
#           v+\
#           '_P.append(np.squeeze(CS[counter].inverse_transform(tmp[counter].reshape(-1,1))))'
#           )
#           counter +=1
#     else:
#        exec(
#        vars[0]+\
#        '_P.append(np.asarray(np.squeeze(CS[0].inverse_transform(tmp.reshape(-1,1)))))'
#        )
#
#     if len(vars)>1:
#        for k in range(len(vars)):
#           exec(
#           vars[k]+\
#           '_pred = np.squeeze(np.mean(np.asarray('+vars[k]+'_P), axis=0))'
#           )
#     else:
#        exec(
#        vars[0]+\
#        '_pred = np.squeeze(np.mean(np.asarray('+vars[0]+'_P), axis=0))'
#        )
#
#
#     if len(vars)==9:
#        nrows = 3; ncols = 3
#     elif len(vars)==8:
#        nrows = 4; ncols = 2
#     elif len(vars)==7:
#        nrows = 4; ncols = 2
#     elif len(vars)==6:
#        nrows = 3; ncols = 2
#     elif len(vars)==5:
#        nrows = 3; ncols = 2
#     elif len(vars)==4:
#        nrows = 2; ncols = 2
#     elif len(vars)==3:
#        nrows = 3; ncols = 1
#     elif len(vars)==2:
#        nrows = 2; ncols = 1
#     elif len(vars)==1:
#        nrows = 1; ncols = 1
#
#     ## make a plot
#     fig = plt.figure(figsize=(4*nrows,4*ncols))
#     labs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#     for k in range(1,1+(nrows*ncols)):
#       plt.subplot(nrows,ncols,k)
#       x = eval(vars[k-1]+'_trueT')
#       y = eval(vars[k-1]+'_predT')
#       plt.plot(x, y, 'ko', markersize=5)
#       plt.plot(eval(vars[k-1]+'_true'), eval(vars[k-1]+'_pred'),
#                'bx', markersize=5)
#       plt.plot([ np.min(np.hstack((x,y))),  np.max(np.hstack((x,y)))],
#                [ np.min(np.hstack((x,y))),  np.max(np.hstack((x,y)))], 'k', lw=2)
#
#       plt.text(np.nanmin(x), 0.96*np.max(np.hstack((x,y))),'Test : '+\
#                str(np.mean(100*(np.abs(eval(vars[k-1]+'_pred') -\
#                 eval(vars[k-1]+'_true')) / eval(vars[k-1]+'_true'))))[:5]+\
#                ' %',  fontsize=8, color='b')
#       plt.text(np.nanmin(x), np.max(np.hstack((x,y))),'Train : '+\
#                str(np.mean(100*(np.abs(eval(vars[k-1]+'_predT') -\
#                 eval(vars[k-1]+'_trueT')) / eval(vars[k-1]+'_trueT'))))[:5]+\
#                ' %', fontsize=8)
#       plt.title(r''+labs[k-1]+') '+vars[k-1], fontsize=8, loc='left')
#
#     varstring = ''.join([str(k)+'_' for k in vars])
#
#     plt.savefig(weights_path.replace('.hdf5', '_skill.png'),
#                 dpi=300, bbox_inches='tight')
#     plt.close()
#     del fig
#

#
# ###===================================================
# def get_data_generator_Nvars_miso_mimo(df, indices, for_training, vars, auxin,
#                                        batch_size, greyscale, CS, CSaux): ##BATCH_SIZE
#     """
#     This function generates data for a batch of images and 1 auxilliary variable,
#     and N associated output metrics
#     """
#     if len(vars)==1:
#        images, a, p1s = [], [], []
#     elif len(vars)==2:
#        images, a, p1s, p2s = [], [], [], []
#     elif len(vars)==3:
#        images, a, p1s, p2s, p3s = [], [], [], [], []
#     elif len(vars)==4:
#        images, a, p1s, p2s, p3s, p4s = [], [], [], [], [], []
#     elif len(vars)==5:
#        images, a, p1s, p2s, p3s, p4s, p5s = [], [], [], [], [], [], []
#     elif len(vars)==6:
#        images, a, p1s, p2s, p3s, p4s, p5s, p6s = \
#        [], [], [], [], [], [], [], []
#     elif len(vars)==7:
#        images, a, p1s, p2s, p3s, p4s, p5s, p6s, p7s = \
#        [], [], [], [], [], [], [], [], []
#     elif len(vars)==8:
#        images, a, p1s, p2s, p3s, p4s, p5s, p6s, p7s, p8s = \
#        [], [], [], [], [], [], [], [], [], []
#     elif len(vars)==9:
#        images, a, p1s, p2s, p3s, p4s, p5s, p6s, p7s, p8s, p9s = \
#        [], [], [], [], [], [], [], [], [], [], []
#
#     while True:
#         for i in indices:
#             r = df.iloc[i]
#             if len(vars)==1:
#                file, p1, aa = r['files'], r[vars[0]], r[auxin]
#             if len(vars)==2:
#                file, p1, p2, aa = \
#                r['files'], r[vars[0]], r[vars[1]], r[auxin]
#             if len(vars)==3:
#                file, p1, p2, p3, aa = \
#                r['files'], r[vars[0]], r[vars[1]], r[vars[2]], r[auxin]
#             if len(vars)==4:
#                file, p1, p2, p3, p4, aa = \
#                r['files'], r[vars[0]], r[vars[1]], r[vars[2]], r[vars[3]], r[auxin]
#             if len(vars)==5:
#                file, p1, p2, p3, p4, p5, aa = \
#                r['files'], r[vars[0]], r[vars[1]], r[vars[2]], r[vars[3]], r[vars[4]], r[auxin]
#             if len(vars)==6:
#                file, p1, p2, p3, p4, p5, p6, aa = \
#                r['files'], r[vars[0]], r[vars[1]], r[vars[2]], r[vars[3]], r[vars[4]], r[vars[5]], r[auxin]
#             if len(vars)==7:
#                file, p1, p2, p3, p4, p5, p6, p7, aa =\
#                r['files'], r[vars[0]], r[vars[1]], r[vars[2]], r[vars[3]], r[vars[4]], r[vars[5]], r[vars[6]], r[auxin]
#             if len(vars)==8:
#                file, p1, p2, p3, p4, p5, p6, p7, p8, aa = \
#                r['files'], r[vars[0]], r[vars[1]], r[vars[2]], r[vars[3]], r[vars[4]], r[vars[5]], r[vars[6]], r[vars[7]], r[auxin]
#             elif len(vars)==9:
#                file, p1, p2, p3, p4, p5, p6, p7, p8, p9, aa = \
#                r['files'], r[vars[0]], r[vars[1]], r[vars[2]], r[vars[3]], r[vars[4]], r[vars[5]], r[vars[6]], r[vars[7]], r[vars[8]], r[auxin]
#
#             if greyscale==True:
#                im = Image.open(file).convert('LA')
#             else:
#                im = Image.open(file)
#             im = im.resize((IM_HEIGHT, IM_HEIGHT))
#             im = np.array(im) / 255.0
#
#             if np.ndim(im)==2:
#                im = np.dstack((im, im , im)) ##np.expand_dims(im[:,:,0], axis=2)
#
#             im = im[:,:,:3]
#
#             if greyscale==True:
#                images.append(np.expand_dims(im, axis=2))
#             else:
#                images.append(im)
#
#             if len(vars)==1:
#                p1s.append(p1); a.append(aa)
#             elif len(vars)==2:
#                p1s.append(p1); p2s.append(p2); a.append(aa)
#             elif len(vars)==3:
#                p1s.append(p1); p2s.append(p2); a.append(aa)
#                p3s.append(p3);
#             elif len(vars)==4:
#                p1s.append(p1); p2s.append(p2); a.append(aa)
#                p3s.append(p3); p4s.append(p4)
#             elif len(vars)==5:
#                p1s.append(p1); p2s.append(p2); a.append(aa)
#                p3s.append(p3); p4s.append(p4)
#                p5s.append(p5);
#             elif len(vars)==6:
#                p1s.append(p1); p2s.append(p2); a.append(aa)
#                p3s.append(p3); p4s.append(p4)
#                p5s.append(p5); p6s.append(p6)
#             elif len(vars)==7:
#                p1s.append(p1); p2s.append(p2); a.append(aa)
#                p3s.append(p3); p4s.append(p4)
#                p5s.append(p5); p6s.append(p6)
#                p7s.append(p7);
#             elif len(vars)==8:
#                p1s.append(p1); p2s.append(p2); a.append(aa)
#                p3s.append(p3); p4s.append(p4)
#                p5s.append(p5); p6s.append(p6)
#                p7s.append(p7); p8s.append(p8)
#             elif len(vars)==9:
#                p1s.append(p1); p2s.append(p2); a.append(aa)
#                p3s.append(p3); p4s.append(p4)
#                p5s.append(p5); p6s.append(p6)
#                p7s.append(p7); p8s.append(p8)
#                p9s.append(p9)
#
#
#             if len(images) >= batch_size:
#                if len(vars)==1:
#                   p1s = np.squeeze(CS[0].transform(np.array(p1s).reshape(-1, 1)))
#                   a = np.squeeze(CSaux[0].transform(np.array(a).reshape(-1, 1)))
#                   yield [np.array(a), np.array(images)], [np.array(p1s)]
#                   images, a, p1s = [], [], []
#                elif len(vars)==2:
#                   p1s = np.squeeze(CS[0].transform(np.array(p1s).reshape(-1, 1)))
#                   p2s = np.squeeze(CS[1].transform(np.array(p2s).reshape(-1, 1)))
#                   a = np.squeeze(CSaux[0].transform(np.array(a).reshape(-1, 1)))
#                   yield [np.array(a), np.array(images)],[np.array(p1s), np.array(p2s)]
#                   images, a, p1s, p2s = [], [], [], []
#                elif len(vars)==3:
#                   p1s = np.squeeze(CS[0].transform(np.array(p1s).reshape(-1, 1)))
#                   p2s = np.squeeze(CS[1].transform(np.array(p2s).reshape(-1, 1)))
#                   p3s = np.squeeze(CS[2].transform(np.array(p3s).reshape(-1, 1)))
#                   a = np.squeeze(CSaux[0].transform(np.array(a).reshape(-1, 1)))
#                   yield [np.array(a), np.array(images)],[np.array(p1s), np.array(p2s), np.array(p3s)]
#                   images, a, p1s, p2s, p3s = [], [], [], [], []
#                elif len(vars)==4:
#                   p1s = np.squeeze(CS[0].transform(np.array(p1s).reshape(-1, 1)))
#                   p2s = np.squeeze(CS[1].transform(np.array(p2s).reshape(-1, 1)))
#                   p3s = np.squeeze(CS[2].transform(np.array(p3s).reshape(-1, 1)))
#                   p4s = np.squeeze(CS[3].transform(np.array(p4s).reshape(-1, 1)))
#                   a = np.squeeze(CSaux[0].transform(np.array(a).reshape(-1, 1)))
#                   yield [np.array(a), np.array(images)],[np.array(p1s), np.array(p2s), np.array(p3s), np.array(p4s)]
#                   images, a, p1s, p2s, p3s, p4s = [], [], [], [], [], []
#                elif len(vars)==5:
#                   p1s = np.squeeze(CS[0].transform(np.array(p1s).reshape(-1, 1)))
#                   p2s = np.squeeze(CS[1].transform(np.array(p2s).reshape(-1, 1)))
#                   p3s = np.squeeze(CS[2].transform(np.array(p3s).reshape(-1, 1)))
#                   p4s = np.squeeze(CS[3].transform(np.array(p4s).reshape(-1, 1)))
#                   p5s = np.squeeze(CS[4].transform(np.array(p5s).reshape(-1, 1)))
#                   a = np.squeeze(CSaux[0].transform(np.array(a).reshape(-1, 1)))
#                   yield [np.array(a), np.array(images)],[np.array(p1s), np.array(p2s), np.array(p3s),
#                         np.array(p4s), np.array(p5s)]
#                   images, a, p1s, p2s, p3s, p4s, p5s = \
#                   [], [], [], [], [], [], []
#                elif len(vars)==6:
#                   p1s = np.squeeze(CS[0].transform(np.array(p1s).reshape(-1, 1)))
#                   p2s = np.squeeze(CS[1].transform(np.array(p2s).reshape(-1, 1)))
#                   p3s = np.squeeze(CS[2].transform(np.array(p3s).reshape(-1, 1)))
#                   p4s = np.squeeze(CS[3].transform(np.array(p4s).reshape(-1, 1)))
#                   p5s = np.squeeze(CS[4].transform(np.array(p5s).reshape(-1, 1)))
#                   p6s = np.squeeze(CS[5].transform(np.array(p6s).reshape(-1, 1)))
#                   a = np.squeeze(CSaux[0].transform(np.array(a).reshape(-1, 1)))
#                   yield [np.array(a), np.array(images)],[np.array(p1s), np.array(p2s), np.array(p3s),
#                         np.array(p4s), np.array(p5s), np.array(p6s)]
#                   images, a, p1s, p2s, p3s, p4s, p5s, p6s = \
#                   [], [], [], [], [], [], [], []
#                elif len(vars)==7:
#                   p1s = np.squeeze(CS[0].transform(np.array(p1s).reshape(-1, 1)))
#                   p2s = np.squeeze(CS[1].transform(np.array(p2s).reshape(-1, 1)))
#                   p3s = np.squeeze(CS[2].transform(np.array(p3s).reshape(-1, 1)))
#                   p4s = np.squeeze(CS[3].transform(np.array(p4s).reshape(-1, 1)))
#                   p5s = np.squeeze(CS[4].transform(np.array(p5s).reshape(-1, 1)))
#                   p6s = np.squeeze(CS[5].transform(np.array(p6s).reshape(-1, 1)))
#                   p7s = np.squeeze(CS[6].transform(np.array(p7s).reshape(-1, 1)))
#                   a = np.squeeze(CSaux[0].transform(np.array(a).reshape(-1, 1)))
#                   yield [np.array(a), np.array(images)],[np.array(p1s), np.array(p2s), np.array(p3s),
#                         np.array(p4s), np.array(p5s), np.array(p6s), np.array(p7s)]
#                   images, a, p1s, p2s, p3s, p4s, p5s, p6s, p7s = \
#                   [], [], [], [], [], [], [], [], []
#                elif len(vars)==8:
#                   p1s = np.squeeze(CS[0].transform(np.array(p1s).reshape(-1, 1)))
#                   p2s = np.squeeze(CS[1].transform(np.array(p2s).reshape(-1, 1)))
#                   p3s = np.squeeze(CS[2].transform(np.array(p3s).reshape(-1, 1)))
#                   p4s = np.squeeze(CS[3].transform(np.array(p4s).reshape(-1, 1)))
#                   p5s = np.squeeze(CS[4].transform(np.array(p5s).reshape(-1, 1)))
#                   p6s = np.squeeze(CS[5].transform(np.array(p6s).reshape(-1, 1)))
#                   p7s = np.squeeze(CS[6].transform(np.array(p7s).reshape(-1, 1)))
#                   p8s = np.squeeze(CS[7].transform(np.array(p8s).reshape(-1, 1)))
#                   a = np.squeeze(CSaux[0].transform(np.array(a).reshape(-1, 1)))
#                   yield [np.array(a), np.array(images)],[np.array(p1s), np.array(p2s), np.array(p3s),
#                         np.array(p4s), np.array(p5s), np.array(p6s),
#                         np.array(p7s), np.array(p8s)]
#                   images, a, p1s, p2s, p3s, p4s, p5s, p6s, p7s, p8s = \
#                   [], [], [], [], [], [], [], [], [], []
#                elif len(vars)==9:
#                   p1s = np.squeeze(CS[0].transform(np.array(p1s).reshape(-1, 1)))
#                   p2s = np.squeeze(CS[1].transform(np.array(p2s).reshape(-1, 1)))
#                   p3s = np.squeeze(CS[2].transform(np.array(p3s).reshape(-1, 1)))
#                   p4s = np.squeeze(CS[3].transform(np.array(p4s).reshape(-1, 1)))
#                   p5s = np.squeeze(CS[4].transform(np.array(p5s).reshape(-1, 1)))
#                   p6s = np.squeeze(CS[5].transform(np.array(p6s).reshape(-1, 1)))
#                   p7s = np.squeeze(CS[6].transform(np.array(p7s).reshape(-1, 1)))
#                   p8s = np.squeeze(CS[7].transform(np.array(p8s).reshape(-1, 1)))
#                   p9s = np.squeeze(CS[8].transform(np.array(p9s).reshape(-1, 1)))
#                   a = np.squeeze(CSaux[0].transform(np.array(a).reshape(-1, 1)))
#                   try:
#                      yield [np.array(a), np.array(images)],[np.array(p1s), np.array(p2s), np.array(p3s),
#                            np.array(p4s), np.array(p5s), np.array(p6s),
#                            np.array(p7s), np.array(p8s), np.array(p9s)]
#                   except GeneratorExit:
#                      print(" ") #pass
#                   images, a, p1s, p2s, p3s, p4s, p5s, p6s, p7s, p8s, p9s = \
#                   [], [], [], [], [], [], [], [], [], [], []
#         if not for_training:
#             break
