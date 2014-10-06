/* ----------------------------------------------------------------- */
/*           The HMM-Based Speech Synthesis Engine "hts_engine API"  */
/*           developed by HTS Working Group                          */
/*           http://hts-engine.sourceforge.net/                      */
/* ----------------------------------------------------------------- */
/*                                                                   */
/*  Copyright (c) 2001-2013  Nagoya Institute of Technology          */
/*                           Department of Computer Science          */
/*                                                                   */
/*                2001-2008  Tokyo Institute of Technology           */
/*                           Interdisciplinary Graduate School of    */
/*                           Science and Engineering                 */
/*                                                                   */
/* All rights reserved.                                              */
/*                                                                   */
/* Redistribution and use in source and binary forms, with or        */
/* without modification, are permitted provided that the following   */
/* conditions are met:                                               */
/*                                                                   */
/* - Redistributions of source code must retain the above copyright  */
/*   notice, this list of conditions and the following disclaimer.   */
/* - Redistributions in binary form must reproduce the above         */
/*   copyright notice, this list of conditions and the following     */
/*   disclaimer in the documentation and/or other materials provided */
/*   with the distribution.                                          */
/* - Neither the name of the HTS working group nor the names of its  */
/*   contributors may be used to endorse or promote products derived */
/*   from this software without specific prior written permission.   */
/*                                                                   */
/* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND            */
/* CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,       */
/* INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF          */
/* MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE          */
/* DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS */
/* BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,          */
/* EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED   */
/* TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,     */
/* DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON */
/* ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,   */
/* OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY    */
/* OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE           */
/* POSSIBILITY OF SUCH DAMAGE.                                       */
/* ----------------------------------------------------------------- */

#ifndef HTS_ENGINE_C
#define HTS_ENGINE_C

#ifdef __cplusplus
#define HTS_ENGINE_C_START extern "C" {
#define HTS_ENGINE_C_END   }
#else
#define HTS_ENGINE_C_START
#define HTS_ENGINE_C_END
#endif                          /* __CPLUSPLUS */

HTS_ENGINE_C_START;

#include <stdlib.h>

#include "HTS_engine.h"

/* usage: output usage */
void usage(void)
{
   fprintf(stderr, "%s\n", HTS_COPYRIGHT);
   fprintf(stderr, "hts_engine - The HMM-based speech synthesis engine \"hts_engine API\"\n");
   fprintf(stderr, "\n");
   fprintf(stderr, "  usage:\n");
   fprintf(stderr, "    hts_engine [ options ] [ infile ]\n");
   fprintf(stderr, "  options:                                                                   [  def][ min-- max]\n");
   fprintf(stderr, "    -m  htsvoice   : HTS voice files                                         [  N/A]\n");
   fprintf(stderr, "    -od s          : filename of output label with duration                  [  N/A]\n");
   fprintf(stderr, "    -om s          : filename of output spectrum                             [  N/A]\n");
   fprintf(stderr, "    -of s          : filename of output log F0                               [  N/A]\n");
   fprintf(stderr, "    -os s          : filename of output bandpass strengths                   [  N/A]\n");
   fprintf(stderr, "    -or s          : filename of output raw audio (generated speech)         [  N/A]\n");
   fprintf(stderr, "    -ow s          : filename of output wav audio (generated speech)         [  N/A]\n");
   fprintf(stderr, "    -ot s          : filename of output trace information                    [  N/A]\n");
   fprintf(stderr, "    -qf            : filename of input log F0 (use instead of predicted)     [  N/A]\n");
   fprintf(stderr, "    -vp            : use phoneme alignment for duration                      [  N/A]\n");
   fprintf(stderr, "    -i  i f1 .. fi : enable interpolation & specify number(i),coefficient(f) [  N/A]\n");
   fprintf(stderr, "    -s  i          : sampling frequency                                      [ auto][   1--    ]\n");
   fprintf(stderr, "    -p  i          : frame period (point)                                    [ auto][   1--    ]\n");
   fprintf(stderr, "    -a  f          : all-pass constant                                       [ auto][ 0.0-- 1.0]\n");
   fprintf(stderr, "    -b  f          : postfiltering coefficient                               [  0.0][ 0.0-- 1.0]\n");
   fprintf(stderr, "    -r  f          : speech speed rate                                       [  1.0][ 0.0--    ]\n");
   fprintf(stderr, "    -fm f          : additional half-tone (not applied if using -qf)         [  0.0][    --    ]\n");
   fprintf(stderr, "    -u  f          : voiced/unvoiced threshold                               [  0.5][ 0.0-- 1.0]\n");
   fprintf(stderr, "    -jm f          : weight of GV for spectrum                               [  1.0][ 0.0--    ]\n");
   fprintf(stderr, "    -jf f          : weight of GV for log F0                                 [  1.0][ 0.0--    ]\n");
   fprintf(stderr, "    -z  i          : audio buffer size (if i==0, turn off)                   [    0][   0--    ]\n");
   fprintf(stderr, "  infile:\n");
   fprintf(stderr, "    label file\n");
   fprintf(stderr, "  note:\n");
   fprintf(stderr, "    generated spectrum, log F0, and bandpass strength\n");
   fprintf(stderr, "    sequences are saved in natural endian, binary (float) format.\n");
   fprintf(stderr, "\n");

   exit(0);
}

int main(int argc, char **argv)
{
   int i, j;
   double f;

   /* hts_engine API */
   HTS_Engine engine;

   /* HTS voices */
   size_t num_voices;
   char **fn_voices;

   /* input label file name */
   char *labfn = NULL;

   /* input lf0 */
   FILE *ilf0fp = NULL;
   double *ilf0 = NULL;
   float *ilf0buffer = NULL; /* just for reading from file */
   size_t ilf0_nframes = 0;
   size_t ilf0_read_nframes = 0;

   /* file names for mixed excitation filters */
   char *me_filter_fn = NULL;
   char *pd_filter_fn = NULL;
   
   /* mixed excitation filters */
   size_t me_num_filters = 0;
   size_t me_filter_order = 0;
   double **me_filter = NULL;
   size_t pd_filter_order = 0;
   double *pd_filter = NULL;
   /* buffers for excitation signals and filters for mixed excitation */
   double *xp_sig = NULL;
   double *xn_sig = NULL;
   double *hp = NULL;
   double *hn = NULL;

   /* output file pointers */
   FILE *durfp = NULL, *mgcfp = NULL, *lf0fp = NULL, *strfp = NULL, *wavfp = NULL, *rawfp = NULL, *tracefp = NULL;

   /* interpolation weights */
   size_t num_interpolation_weights;

   /* output usage */
   if (argc <= 1)
      usage();

   /* initialize hts_engine API */
   HTS_Engine_initialize(&engine);

   /* get HTS voice file names */
   num_voices = 0;
   fn_voices = (char **) malloc(argc * sizeof(char *));
   for (i = 0; i < argc; i++) {
      if (argv[i][0] == '-' && argv[i][1] == 'm')
         fn_voices[num_voices++] = argv[++i];
      if (argv[i][0] == '-' && argv[i][1] == 'h')
         usage();
   }
   if (num_voices == 0) {
      fprintf(stderr, "Error: HTS voice must be specified.\n");
      free(fn_voices);
      exit(1);
   }

   /* load HTS voices */
   if (HTS_Engine_load(&engine, fn_voices, num_voices) != TRUE) {
      fprintf(stderr, "Error: HTS voices cannot be loaded.\n");
      free(fn_voices);
      HTS_Engine_clear(&engine);
      exit(1);
   }
   free(fn_voices);

   /* get options */
   while (--argc) {
      if (**++argv == '-') {
         switch (*(*argv + 1)) {
         case 'v':
            switch (*(*argv + 2)) {
            case 'p':
               HTS_Engine_set_phoneme_alignment_flag(&engine, TRUE);
               break;
            default:
               fprintf(stderr, "Error: Invalid option '-v%c'.\n", *(*argv + 2));
               HTS_Engine_clear(&engine);
               exit(1);
            }
            break;
	 case 'q':
	    switch (*(*argv + 2)) {
	    case 'f':
	       ilf0fp = fopen(*++argv, "rb");
	       /* determine file size */
	       fseek(ilf0fp, 0, SEEK_END);
	       ilf0_nframes = (size_t) (ftell(ilf0fp) / sizeof(float)); 
	       /* fprintf(stderr, "Counted %lu frames in ilf0 file.\n", (unsigned long)ilf0_nframes); */
	       fseek(ilf0fp, 0, SEEK_SET);
	       /* allocate and read */
	       ilf0buffer = calloc(ilf0_nframes, sizeof(float));
	       ilf0_read_nframes = fread(ilf0buffer, sizeof(float), ilf0_nframes, ilf0fp);
	       fclose(ilf0fp);
	       if (ilf0_read_nframes != ilf0_nframes) {
		  fprintf(stderr, "Error reading lf0 from file (-qf).");
		  HTS_Engine_clear(&engine);
		  free(ilf0buffer);
		  exit(1);
	       }
	       /* cast to double */
	       ilf0 = calloc(ilf0_nframes, sizeof(double));
	       for (j = 0; j < ilf0_read_nframes; j++)
		  ilf0[j] = (double)ilf0buffer[j];
	       free(ilf0buffer);
	       break;
	    default:
               fprintf(stderr, "Error: Invalid option '-q%c'.\n", *(*argv + 2));
               HTS_Engine_clear(&engine);
               exit(1);
	    }
	    --argc;
	    break;
	 case 'x':
	    switch (*(*argv + 2)) {
	    case 'm':
	       me_filter_fn = *++argv;
	       break;
	    case 'p':
	       pd_filter_fn = *++argv;
	       break;
	    default:
	       fprintf(stderr, "Error: Invalid option '-x%c'.\n", *(*argv + 2));
	       HTS_Engine_clear(&engine);
	       exit(1);
	    }
	    --argc;
	    break;
         case 'o':
            switch (*(*argv + 2)) {
            case 'w':
               wavfp = fopen(*++argv, "wb");
               break;
            case 'r':
               rawfp = fopen(*++argv, "wb");
               break;
            case 'd':
               durfp = fopen(*++argv, "wt");
               break;
            case 'm':
               mgcfp = fopen(*++argv, "wb");
               break;
            case 'f':
            case 'p':
               lf0fp = fopen(*++argv, "wb");
               break;
            case 's':
               strfp = fopen(*++argv, "wb");
               break;
            case 't':
               tracefp = fopen(*++argv, "wt");
               break;
            default:
               fprintf(stderr, "Error: Invalid option '-o%c'.\n", *(*argv + 2));
               HTS_Engine_clear(&engine);
               exit(1);
            }
            --argc;
            break;
         case 'h':
            usage();
            break;
         case 'm':
            argv++;             /* HTS voices were already loaded */
            --argc;
            break;
         case 's':
            HTS_Engine_set_sampling_frequency(&engine, (size_t) atoi(*++argv));
            --argc;
            break;
         case 'p':
            HTS_Engine_set_fperiod(&engine, (size_t) atoi(*++argv));
            --argc;
            break;
         case 'a':
            HTS_Engine_set_alpha(&engine, atof(*++argv));
            --argc;
            break;
         case 'b':
            HTS_Engine_set_beta(&engine, atof(*++argv));
            --argc;
            break;
         case 'r':
            HTS_Engine_set_speed(&engine, atof(*++argv));
            --argc;
            break;
         case 'f':
            switch (*(*argv + 2)) {
            case 'm':
               HTS_Engine_add_half_tone(&engine, atof(*++argv));
               break;
            default:
               fprintf(stderr, "Error: Invalid option '-f%c'.\n", *(*argv + 2));
               HTS_Engine_clear(&engine);
               exit(1);
            }
            --argc;
            break;
         case 'u':
            HTS_Engine_set_msd_threshold(&engine, 1, atof(*++argv));
            --argc;
            break;
         case 'i':
            num_interpolation_weights = atoi(*++argv);
            argc--;
            if (num_interpolation_weights != num_voices) {
               HTS_Engine_clear(&engine);
               exit(1);
            }
            for (i = 0; i < num_interpolation_weights; i++) {
               f = atof(*++argv);
               argc--;
               HTS_Engine_set_duration_interpolation_weight(&engine, i, f);
               HTS_Engine_set_parameter_interpolation_weight(&engine, i, 0, f);
               HTS_Engine_set_parameter_interpolation_weight(&engine, i, 1, f);
               HTS_Engine_set_gv_interpolation_weight(&engine, i, 0, f);
               HTS_Engine_set_gv_interpolation_weight(&engine, i, 1, f);
            }
            break;
         case 'j':
            switch (*(*argv + 2)) {
            case 'm':
               HTS_Engine_set_gv_weight(&engine, 0, atof(*++argv));
               break;
            case 'f':
            case 'p':
               HTS_Engine_set_gv_weight(&engine, 1, atof(*++argv));
               break;
            default:
               fprintf(stderr, "Error: Invalid option '-j%c'.\n", *(*argv + 2));
               HTS_Engine_clear(&engine);
               exit(1);
            }
            --argc;
            break;
         default:
            fprintf(stderr, "Error: Invalid option '-%c'.\n", *(*argv + 1));
            HTS_Engine_clear(&engine);
            exit(1);
         }
      } else {
         labfn = *argv;
      }
   }

   /* DEMITASSE: In future this should be part of HTS_Engine initialisation? */
   /* load filters for mixed excitation synthesis*/
   if (me_filter_fn != NULL && pd_filter_fn != NULL) {
      HTS_Engine_load_me_filter_from_fn(me_filter_fn, &me_filter, &me_num_filters, &me_filter_order);
      HTS_Engine_load_pd_filter_from_fn(pd_filter_fn, &pd_filter, &pd_filter_order);
   } else {
      fprintf(stderr, "Error: Need to specify bandpass and pulse dispersion filters for mixed excitation synthesis");
      HTS_Engine_clear(&engine);
      exit(1);
   }

   /* DEMITASSE: In future this should be part of HTS_Engine initialisation? */
   /* allocate buffers for excitation components and filter coefficients */
   xp_sig =  calloc(me_filter_order, sizeof(double));
   xn_sig = calloc(me_filter_order, sizeof(double));
   hp = calloc(me_filter_order, sizeof(double));
   hn = calloc(me_filter_order, sizeof(double));

   /* synthesize */
   if (HTS_Engine_synthesize_me_with_lf0_from_fn(&engine, labfn, me_num_filters, me_filter_order, me_filter, pd_filter_order, pd_filter, xp_sig, xn_sig, hp, hn, ilf0, ilf0_nframes) != TRUE) {
      fprintf(stderr, "Error: waveform cannot be synthesized.\n");
      HTS_Engine_clear(&engine);
      if (ilf0 != NULL)
	 free(ilf0);
      if (me_filter != NULL)
	 free(me_filter);
      if (pd_filter != NULL)
	 free(pd_filter);
      if (xp_sig != NULL)
	 free(xp_sig);
      if (xn_sig != NULL)
	 free(xn_sig);
      if (hp != NULL)
	 free(hp);
      if (hn != NULL)
	 free(hn);
      exit(1);
   }

   /* output */
   if (tracefp != NULL)
      HTS_Engine_save_information(&engine, tracefp);
   if (durfp != NULL)
      HTS_Engine_save_label(&engine, durfp);
   if (rawfp)
      HTS_Engine_save_generated_speech(&engine, rawfp);
   if (wavfp)
      HTS_Engine_save_riff(&engine, wavfp);
   if (mgcfp)
      HTS_Engine_save_generated_parameter(&engine, 0, mgcfp);
   if (lf0fp)
      HTS_Engine_save_generated_parameter(&engine, 1, lf0fp);
   if (strfp)
      HTS_Engine_save_generated_parameter(&engine, 2, strfp);

   /* reset */
   HTS_Engine_refresh(&engine);

   /* free memory */
   HTS_Engine_clear(&engine);
   if (ilf0 != NULL)
      free(ilf0);
   if (me_filter != NULL)
      free(me_filter);
   if (pd_filter != NULL)
      free(pd_filter);
   if (xp_sig != NULL)
      free(xp_sig);
   if (xn_sig != NULL)
      free(xn_sig);
   if (hp != NULL)
      free(hp);
   if (hn != NULL)
      free(hn);
   
   /* close files */
   if (durfp != NULL)
      fclose(durfp);
   if (mgcfp != NULL)
      fclose(mgcfp);
   if (lf0fp != NULL)
      fclose(lf0fp);
   if (strfp != NULL)
      fclose(strfp);
   if (wavfp != NULL)
      fclose(wavfp);
   if (rawfp != NULL)
      fclose(rawfp);
   if (tracefp != NULL)
      fclose(tracefp);

   return 0;
}

HTS_ENGINE_C_END;

#endif                          /* !HTS_ENGINE_C */
