typedef char HTS_Boolean;

/* HTS_Audio: audio output wrapper */
typedef struct _HTS_Audio {
   size_t sampling_frequency;   /* sampling frequency */
   size_t max_buff_size;        /* buffer size for audio output interface */
   short *buff;                 /* current buffer */
   size_t buff_size;            /* current buffer size */
   void *audio_interface;       /* audio interface specified in compile step */
} HTS_Audio;

/* model ----------------------------------------------------------- */

/* HTS_Window: window coefficients to calculate dynamic features. */
typedef struct _HTS_Window {
   size_t size;                 /* # of windows (static + deltas) */
   int *l_width;                /* left width of windows */
   int *r_width;                /* right width of windows */
   double **coefficient;        /* window coefficient */
   size_t max_width;            /* maximum width of windows */
} HTS_Window;

/* HTS_Pattern: list of patterns in a question and a tree. */
typedef struct _HTS_Pattern {
   char *string;                /* pattern string */
   struct _HTS_Pattern *next;   /* pointer to the next pattern */
} HTS_Pattern;

/* HTS_Question: list of questions in a tree. */
typedef struct _HTS_Question {
   char *string;                /* name of this question */
   HTS_Pattern *head;           /* pointer to the head of pattern list */
   struct _HTS_Question *next;  /* pointer to the next question */
} HTS_Question;

/* HTS_Node: list of tree nodes in a tree. */
typedef struct _HTS_Node {
   int index;                   /* index of this node */
   size_t pdf;                  /* index of PDF for this node (leaf node only) */
   struct _HTS_Node *yes;       /* pointer to its child node (yes) */
   struct _HTS_Node *no;        /* pointer to its child node (no) */
   struct _HTS_Node *next;      /* pointer to the next node */
   HTS_Question *quest;         /* question applied at this node */
} HTS_Node;

/* HTS_Tree: list of decision trees in a model. */
typedef struct _HTS_Tree {
   HTS_Pattern *head;           /* pointer to the head of pattern list for this tree */
   struct _HTS_Tree *next;      /* pointer to next tree */
   HTS_Node *root;              /* root node of this tree */
   size_t state;                /* state index of this tree */
} HTS_Tree;

/* HTS_Model: set of PDFs, decision trees and questions. */
typedef struct _HTS_Model {
   size_t vector_length;        /* vector length (static features only) */
   size_t num_windows;          /* # of windows for delta */
   HTS_Boolean is_msd;          /* flag for MSD */
   size_t ntree;                /* # of trees */
   size_t *npdf;                /* # of PDFs at each tree */
   float ***pdf;                /* PDFs */
   HTS_Tree *tree;              /* pointer to the list of trees */
   HTS_Question *question;      /* pointer to the list of questions */
} HTS_Model;

/* HTS_ModelSet: set of duration models, HMMs and GV models. */
typedef struct _HTS_ModelSet {
   char *hts_voice_version;     /* version of HTS voice format */
   size_t sampling_frequency;   /* sampling frequency */
   size_t frame_period;         /* frame period */
   size_t num_voices;           /* # of HTS voices */
   size_t num_states;           /* # of HMM states */
   size_t num_streams;          /* # of streams */
   char *stream_type;           /* stream type */
   char *fullcontext_format;    /* fullcontext label format */
   char *fullcontext_version;   /* version of fullcontext label */
   HTS_Question *gv_off_context;        /* GV switch */
   char **option;               /* options for each stream */
   HTS_Model *duration;         /* duration PDFs and trees */
   HTS_Window *window;          /* window coefficients for delta */
   HTS_Model **stream;          /* parameter PDFs and trees */
   HTS_Model **gv;              /* GV PDFs and trees */
} HTS_ModelSet;

/* label ----------------------------------------------------------- */

/* HTS_LabelString: individual label string with time information */
typedef struct _HTS_LabelString {
   struct _HTS_LabelString *next;       /* pointer to next label string */
   char *name;                  /* label string */
   double start;                /* start frame specified in the given label */
   double end;                  /* end frame specified in the given label */
} HTS_LabelString;

/* HTS_Label: list of label strings */
typedef struct _HTS_Label {
   HTS_LabelString *head;       /* pointer to the head of label string */
   size_t size;                 /* # of label strings */
} HTS_Label;

/* sstream --------------------------------------------------------- */

/* HTS_SStream: individual state stream */
typedef struct _HTS_SStream {
   size_t vector_length;        /* vector length (static features only) */
   double **mean;               /* mean vector sequence */
   double **vari;               /* variance vector sequence */
   double *msd;                 /* MSD parameter sequence */
   size_t win_size;             /* # of windows (static + deltas) */
   int *win_l_width;            /* left width of windows */
   int *win_r_width;            /* right width of windows */
   double **win_coefficient;    /* window cofficients */
   size_t win_max_width;        /* maximum width of windows */
   double *gv_mean;             /* mean vector of GV */
   double *gv_vari;             /* variance vector of GV */
   HTS_Boolean *gv_switch;      /* GV flag sequence */
} HTS_SStream;

/* HTS_SStreamSet: set of state stream */
typedef struct _HTS_SStreamSet {
   HTS_SStream *sstream;        /* state streams */
   size_t nstream;              /* # of streams */
   size_t nstate;               /* # of states */
   size_t *duration;            /* duration sequence */
   size_t total_state;          /* total state */
   size_t total_frame;          /* total frame */
} HTS_SStreamSet;

/* pstream --------------------------------------------------------- */

/* HTS_SMatrices: matrices/vectors used in the speech parameter generation algorithm. */
typedef struct _HTS_SMatrices {
   double **mean;               /* mean vector sequence */
   double **ivar;               /* inverse diag variance sequence */
   double *g;                   /* vector used in the forward substitution */
   double **wuw;                /* W' U^-1 W  */
   double *wum;                 /* W' U^-1 mu */
} HTS_SMatrices;

/* HTS_PStream: individual PDF stream. */
typedef struct _HTS_PStream {
   size_t vector_length;        /* vector length (static features only) */
   size_t length;               /* stream length */
   size_t width;                /* width of dynamic window */
   double **par;                /* output parameter vector */
   HTS_SMatrices sm;            /* matrices for parameter generation */
   size_t win_size;             /* # of windows (static + deltas) */
   int *win_l_width;            /* left width of windows */
   int *win_r_width;            /* right width of windows */
   double **win_coefficient;    /* window coefficients */
   HTS_Boolean *msd_flag;       /* Boolean sequence for MSD */
   double *gv_mean;             /* mean vector of GV */
   double *gv_vari;             /* variance vector of GV */
   HTS_Boolean *gv_switch;      /* GV flag sequence */
   size_t gv_length;            /* frame length for GV calculation */
} HTS_PStream;

/* HTS_PStreamSet: set of PDF streams. */
typedef struct _HTS_PStreamSet {
   HTS_PStream *pstream;        /* PDF streams */
   size_t nstream;              /* # of PDF streams */
   size_t total_frame;          /* total frame */
} HTS_PStreamSet;

/* gstream --------------------------------------------------------- */

/* HTS_GStream: generated parameter stream. */
typedef struct _HTS_GStream {
   size_t vector_length;        /* vector length (static features only) */
   double **par;                /* generated parameter */
} HTS_GStream;

/* HTS_GStreamSet: set of generated parameter stream. */
typedef struct _HTS_GStreamSet {
   size_t total_nsample;        /* total sample */
   size_t total_frame;          /* total frame */
   size_t nstream;              /* # of streams */
   HTS_GStream *gstream;        /* generated parameter streams */
   double *gspeech;             /* generated speech */
} HTS_GStreamSet;

/* engine ---------------------------------------------------------- */

/* HTS_Condition: synthesis condition */
typedef struct _HTS_Condition {
   /* global */
   size_t sampling_frequency;   /* sampling frequency */
   size_t fperiod;              /* frame period */
   size_t audio_buff_size;      /* audio buffer size (for audio device) */
   HTS_Boolean stop;            /* stop flag */
   double volume;               /* volume */
   double *msd_threshold;       /* MSD thresholds */
   double *gv_weight;           /* GV weights */

   /* duration */
   HTS_Boolean phoneme_alignment_flag;  /* flag for using phoneme alignment in label */
   double speed;                /* speech speed */

   /* spectrum */
   size_t stage;                /* if stage=0 then gamma=0 else gamma=-1/stage */
   HTS_Boolean use_log_gain;    /* log gain flag (for LSP) */
   double alpha;                /* all-pass constant */
   double beta;                 /* postfiltering coefficient */

   /* log F0 */
   double additional_half_tone; /* additional half tone */

   /* interpolation weights */
   double *duration_iw;         /* weights for duration interpolation */
   double **parameter_iw;       /* weights for parameter interpolation */
   double **gv_iw;              /* weights for GV interpolation */
} HTS_Condition;

/* HTS_Engine: Engine itself. */
typedef struct _HTS_Engine {
   HTS_Condition condition;     /* synthesis condition */
   HTS_Audio audio;             /* audio output */
   HTS_ModelSet ms;             /* set of duration models, HMMs and GV models */
   HTS_Label label;             /* label */
   HTS_SStreamSet sss;          /* set of state streams */
   HTS_PStreamSet pss;          /* set of PDF streams */
   HTS_GStreamSet gss;          /* set of generated parameter streams */
} HTS_Engine;

/* engine method --------------------------------------------------- */

/* HTS_Engine_initialize: initialize engine */
void HTS_Engine_initialize(HTS_Engine * engine);

/* HTS_Engine_load: load HTS voices */
HTS_Boolean HTS_Engine_load(HTS_Engine * engine, char **voices, size_t num_voices);

/* HTS_Engine_set_sampling_frequency: set sampling fraquency */
void HTS_Engine_set_sampling_frequency(HTS_Engine * engine, size_t i);

/* HTS_Engine_get_sampling_frequency: get sampling frequency */
size_t HTS_Engine_get_sampling_frequency(HTS_Engine * engine);

/* HTS_Engine_set_fperiod: set frame period */
void HTS_Engine_set_fperiod(HTS_Engine * engine, size_t i);

/* HTS_Engine_get_fperiod: get frame period */
size_t HTS_Engine_get_fperiod(HTS_Engine * engine);

/* HTS_Engine_set_audio_buff_size: set audio buffer size */
void HTS_Engine_set_audio_buff_size(HTS_Engine * engine, size_t i);

/* HTS_Engine_get_audio_buff_size: get audio buffer size */
size_t HTS_Engine_get_audio_buff_size(HTS_Engine * engine);

/* HTS_Engine_set_stop_flag: set stop flag */
void HTS_Engine_set_stop_flag(HTS_Engine * engine, HTS_Boolean b);

/* HTS_Engine_get_stop_flag: get stop flag */
HTS_Boolean HTS_Engine_get_stop_flag(HTS_Engine * engine);

/* HTS_Engine_set_volume: set volume in db */
void HTS_Engine_set_volume(HTS_Engine * engine, double f);

/* HTS_Engine_get_volume: get volume in db */
double HTS_Engine_get_volume(HTS_Engine * engine);

/* HTS_Egnine_set_msd_threshold: set MSD threshold */
void HTS_Engine_set_msd_threshold(HTS_Engine * engine, size_t stream_index, double f);

/* HTS_Engine_get_msd_threshold: get MSD threshold */
double HTS_Engine_get_msd_threshold(HTS_Engine * engine, size_t stream_index);

/* HTS_Engine_set_gv_weight: set GV weight */
void HTS_Engine_set_gv_weight(HTS_Engine * engine, size_t stream_index, double f);

/* HTS_Engine_get_gv_weight: get GV weight */
double HTS_Engine_get_gv_weight(HTS_Engine * engine, size_t stream_index);

/* HTS_Engine_set_speed: set speech speed */
void HTS_Engine_set_speed(HTS_Engine * engine, double f);

/* HTS_Engine_set_phoneme_alignment_flag: set flag for using phoneme alignment in label */
void HTS_Engine_set_phoneme_alignment_flag(HTS_Engine * engine, HTS_Boolean b);

/* HTS_Engine_set_alpha: set alpha */
void HTS_Engine_set_alpha(HTS_Engine * engine, double f);

/* HTS_Engine_get_alpha: get alpha */
double HTS_Engine_get_alpha(HTS_Engine * engine);

/* HTS_Engine_set_beta: set beta */
void HTS_Engine_set_beta(HTS_Engine * engine, double f);

/* HTS_Engine_get_beta: get beta */
double HTS_Engine_get_beta(HTS_Engine * engine);

/* HTS_Engine_add_half_tone: add half tone */
void HTS_Engine_add_half_tone(HTS_Engine * engine, double f);

/* HTS_Engine_set_duration_interpolation_weight: set interpolation weight for duration */
void HTS_Engine_set_duration_interpolation_weight(HTS_Engine * engine, size_t voice_index, double f);

/* HTS_Engine_get_duration_interpolation_weight: get interpolation weight for duration */
double HTS_Engine_get_duration_interpolation_weight(HTS_Engine * engine, size_t voice_index);

/* HTS_Engine_set_parameter_interpolation_weight: set interpolation weight for parameter */
void HTS_Engine_set_parameter_interpolation_weight(HTS_Engine * engine, size_t voice_index, size_t stream_index, double f);

/* HTS_Engine_get_parameter_interpolation_weight: get interpolation weight for parameter */
double HTS_Engine_get_parameter_interpolation_weight(HTS_Engine * engine, size_t voice_index, size_t stream_index);

/* HTS_Engine_set_gv_interpolation_weight: set interpolation weight for GV */
void HTS_Engine_set_gv_interpolation_weight(HTS_Engine * engine, size_t voice_index, size_t stream_index, double f);

/* HTS_Engine_get_gv_interpolation_weight: get interpolation weight for GV */
double HTS_Engine_get_gv_interpolation_weight(HTS_Engine * engine, size_t voice_index, size_t stream_index);

/* HTS_Engine_get_total_state: get total number of state */
size_t HTS_Engine_get_total_state(HTS_Engine * engine);

/* HTS_Engine_set_state_mean: set mean value of state */
void HTS_Engine_set_state_mean(HTS_Engine * engine, size_t stream_index, size_t state_index, size_t vector_index, double f);

/* HTS_Engine_get_state_mean: get mean value of state */
double HTS_Engine_get_state_mean(HTS_Engine * engine, size_t stream_index, size_t state_index, size_t vector_index);

/* HTS_Engine_get_state_duration: get state duration */
size_t HTS_Engine_get_state_duration(HTS_Engine * engine, size_t state_index);

/* HTS_Engine_get_nvoices: get number of voices */
size_t HTS_Engine_get_nvoices(HTS_Engine * engine);

/* HTS_Engine_get_nstream: get number of stream */
size_t HTS_Engine_get_nstream(HTS_Engine * engine);

/* HTS_Engine_get_nstate: get number of state */
size_t HTS_Engine_get_nstate(HTS_Engine * engine);

/* HTS_Engine_get_total_frame: get total number of frame */
size_t HTS_Engine_get_total_frame(HTS_Engine * engine);

/* HTS_Engine_get_nsamples: get number of samples */
size_t HTS_Engine_get_nsamples(HTS_Engine * engine);

/* HTS_Engine_get_generated_parameter: output generated parameter */
double HTS_Engine_get_generated_parameter(HTS_Engine * engine, size_t stream_index, size_t frame_index, size_t vector_index);

/* HTS_Engine_get_generated_speech: output generated speech */
double HTS_Engine_get_generated_speech(HTS_Engine * engine, size_t index);

/* HTS_Engine_synthesize_from_fn: synthesize speech from file name */
HTS_Boolean HTS_Engine_synthesize_from_fn(HTS_Engine * engine, const char *fn);

/* HTS_Engine_synthesize_me_with_lf0_from_fn: synthesize speech by replacing the generated lf0 with ilf0 before vocoding */
HTS_Boolean HTS_Engine_synthesize_me_with_lf0_from_fn(HTS_Engine * engine, const char *fn, size_t me_num_filters, size_t me_filter_order, const double ** me_filter, size_t pd_filter_order, const double * pd_filter, double * xp_sig, double * xn_sig, double * hp, double * hn, const double * ilf0, size_t ilf0_nframes);

/* HTS_Engine_synthesize_from_strings: synthesize speech from string list */
HTS_Boolean HTS_Engine_synthesize_from_strings(HTS_Engine * engine, char **lines, size_t num_lines);

/* HTS_Engine_synthesize_me_with_lf0_from_strings: synthesize speech from string list by replacing the generated lf0 with ilf0 before vocoding */
HTS_Boolean HTS_Engine_synthesize_me_with_lf0_from_strings(HTS_Engine * engine, char **lines, size_t num_lines, size_t me_num_filters, size_t me_filter_order, const double ** me_filter, size_t pd_filter_order, const double * pd_filter, double * xp_sig, double * xn_sig, double * hp, double * hn, const double * ilf0, size_t ilf0_nframes);

/* HTS_Engine_generate_state_sequence_from_fn: generate state sequence from file name (1st synthesis step) */
HTS_Boolean HTS_Engine_generate_state_sequence_from_fn(HTS_Engine * engine, const char *fn);

/* HTS_Engine_generate_state_sequence_from_strings: generate state sequence from string list (1st synthesis step) */
HTS_Boolean HTS_Engine_generate_state_sequence_from_strings(HTS_Engine * engine, char **lines, size_t num_lines);

/* HTS_Engine_generate_parameter_sequence: generate parameter sequence (2nd synthesis step) */
HTS_Boolean HTS_Engine_generate_parameter_sequence(HTS_Engine * engine);

/* HTS_Engine_generate_sample_sequence: generate sample sequence (3rd synthesis step) */
HTS_Boolean HTS_Engine_generate_sample_sequence(HTS_Engine * engine);

/* HTS_Engine_generate_sample_sequence_me_with_lf0: generate sample sequence (3rd synthesis step), replacing lf0 with ilf0 before vocoding*/
HTS_Boolean HTS_Engine_generate_sample_sequence_me_with_lf0(HTS_Engine * engine, size_t me_num_filters, size_t me_filter_order, const double ** me_filter, size_t pd_filter_order, const double * pd_filter, double * xp_sig, double * xn_sig, double * hp, double * hn, const double * ilf0, size_t ilf0_nframes);

/* HTS_Engine_save_information: save trace information */
void HTS_Engine_save_information(HTS_Engine * engine, FILE * fp);

/* HTS_Engine_save_label: save label with time */
void HTS_Engine_save_label(HTS_Engine * engine, FILE * fp);

/* HTS_Engine_save_generated_parameter: save generated parameter */
void HTS_Engine_save_generated_parameter(HTS_Engine * engine, size_t stream_index, FILE * fp);

/* HTS_Engine_save_generated_speech: save generated speech */
void HTS_Engine_save_generated_speech(HTS_Engine * engine, FILE * fp);

/* HTS_Engine_save_riff: save RIFF format file */
void HTS_Engine_save_riff(HTS_Engine * engine, FILE * fp);

/* HTS_Engine_refresh: free memory per one time synthesis */
void HTS_Engine_refresh(HTS_Engine * engine);

/* HTS_Engine_clear: free engine */
void HTS_Engine_clear(HTS_Engine * engine);

/* HTS_Engine_load_me_filter_from_fn: load mixed excitation filter from file name */
void HTS_Engine_load_me_filter_from_fn(char *me_filter_fn, double ***me_filter, size_t *me_num_filters, size_t *me_filter_order);

/* HTS_Engine_load_pd_filter_from_fn: load pulse dispersion filter from file name */
void HTS_Engine_load_pd_filter_from_fn(char *pd_filter_fn, double **pd_filter, size_t *pd_filter_order);

typedef struct _HTS_File {
   unsigned char type;
   void *pointer;
} HTS_File;

/* HTS_fopen: wrapper for fopen */
HTS_File *HTS_fopen_from_fn(const char *name, const char *opt);

/* HTS_fopen_from_fp: wrapper for fopen */
HTS_File *HTS_fopen_from_fp(HTS_File * fp, size_t size);

/* HTS_fopen_from_data: wrapper for fopen */
HTS_File *HTS_fopen_from_data(void *data, size_t size);

/* HTS_fclose: wrapper for fclose */
void HTS_fclose(HTS_File * fp);

/* HTS_fgetc: wrapper for fgetc */
int HTS_fgetc(HTS_File * fp);

/* HTS_feof: wrapper for feof */
int HTS_feof(HTS_File * fp);

/* HTS_fseek: wrapper for fseek */
int HTS_fseek(HTS_File * fp, long offset, int origin);

/* HTS_ftell: wrapper for ftell */
size_t HTS_ftell(HTS_File * fp);

/* HTS_fread_big_endiana: fread with byteswap */
size_t HTS_fread_big_endian(void *buf, size_t size, size_t n, HTS_File * fp);

/* HTS_fread_little_endiana: fread with byteswap */
size_t HTS_fread_little_endian(void *buf, size_t size, size_t n, HTS_File * fp);

/* HTS_fwrite_little_endian: fwrite with byteswap */
size_t HTS_fwrite_little_endian(const void *buf, size_t size, size_t n, FILE * fp);

/* HTS_get_pattern_token: get pattern token (single/double quote can be used) */
HTS_Boolean HTS_get_pattern_token(HTS_File * fp, char *buff);

/* HTS_get_token: get token from file pointer (separators are space,tab,line break) */
HTS_Boolean HTS_get_token_from_fp(HTS_File * fp, char *buff);

/* HTS_get_token: get token from file pointer with specified separator */
HTS_Boolean HTS_get_token_from_fp_with_separator(HTS_File * fp, char *buff, char separator);

/* HTS_get_token_from_string: get token from string (separator are space,tab,line break) */
HTS_Boolean HTS_get_token_from_string(const char *string, size_t * index, char *buff);

/* HTS_get_token_from_string_with_separator: get token from string with specified separator */
HTS_Boolean HTS_get_token_from_string_with_separator(const char *str, size_t * index, char *buff, char separator);

/* HTS_calloc: wrapper for calloc */
void *HTS_calloc(const size_t num, const size_t size);

/* HTS_strdup: wrapper for strdup */
char *HTS_strdup(const char *string);

/* HTS_calloc_matrix: allocate double matrix */
double **HTS_alloc_matrix(size_t x, size_t y);

/* HTS_free_matrix: free double matrix */
void HTS_free_matrix(double **p, size_t x);

/* HTS_Free: wrapper for free */
void HTS_free(void *p);

/* HTS_error: output error message */
void HTS_error(int error, const char *message, ...);

/* audio ----------------------------------------------------------- */

/* HTS_Audio_initialize: initialize audio */
void HTS_Audio_initialize(HTS_Audio * audio);

/* HTS_Audio_set_parameter: set parameters for audio */
void HTS_Audio_set_parameter(HTS_Audio * audio, size_t sampling_frequency, size_t max_buff_size);

/* HTS_Audio_write: send data to audio */
void HTS_Audio_write(HTS_Audio * audio, short data);

/* HTS_Audio_flush: flush remain data */
void HTS_Audio_flush(HTS_Audio * audio);

/* HTS_Audio_clear: free audio */
void HTS_Audio_clear(HTS_Audio * audio);

/* model ----------------------------------------------------------- */

/* HTS_ModelSet_initialize: initialize model set */
void HTS_ModelSet_initialize(HTS_ModelSet * ms);

/* HTS_ModelSet_load: load HTS voices */
HTS_Boolean HTS_ModelSet_load(HTS_ModelSet * ms, char **voices, size_t num_voices);

/* HTS_ModelSet_get_sampling_frequency: get sampling frequency of HTS voices */
size_t HTS_ModelSet_get_sampling_frequency(HTS_ModelSet * ms);

/* HTS_ModelSet_get_fperiod: get frame period of HTS voices */
size_t HTS_ModelSet_get_fperiod(HTS_ModelSet * ms);

/* HTS_ModelSet_get_fperiod: get stream option */
const char *HTS_ModelSet_get_option(HTS_ModelSet * ms, size_t stream_index);

/* HTS_ModelSet_get_gv_flag: get GV flag */
HTS_Boolean HTS_ModelSet_get_gv_flag(HTS_ModelSet * ms, const char *string);

/* HTS_ModelSet_get_nstate: get number of state */
size_t HTS_ModelSet_get_nstate(HTS_ModelSet * ms);

/* HTS_ModelSet_get_nstream: get number of stream */
size_t HTS_ModelSet_get_nstream(HTS_ModelSet * ms);

/* HTS_ModelSet_get_nvoices: get number of HTS voices */
size_t HTS_ModelSet_get_nvoices(HTS_ModelSet * ms);

/* HTS_ModelSet_get_vector_length: get vector length */
size_t HTS_ModelSet_get_vector_length(HTS_ModelSet * ms, size_t stream_index);

/* HTS_ModelSet_is_msd: get MSD flag */
HTS_Boolean HTS_ModelSet_is_msd(HTS_ModelSet * ms, size_t stream_index);

/* HTS_ModelSet_get_window_size: get dynamic window size */
size_t HTS_ModelSet_get_window_size(HTS_ModelSet * ms, size_t stream_index);

/* HTS_ModelSet_get_window_left_width: get left width of dynamic window */
int HTS_ModelSet_get_window_left_width(HTS_ModelSet * ms, size_t stream_index, size_t window_index);

/* HTS_ModelSet_get_window_right_width: get right width of dynamic window */
int HTS_ModelSet_get_window_right_width(HTS_ModelSet * ms, size_t stream_index, size_t window_index);

/* HTS_ModelSet_get_window_coefficient: get coefficient of dynamic window */
double HTS_ModelSet_get_window_coefficient(HTS_ModelSet * ms, size_t stream_index, size_t window_index, size_t coefficient_index);

/* HTS_ModelSet_get_window_max_width: get max width of dynamic window */
size_t HTS_ModelSet_get_window_max_width(HTS_ModelSet * ms, size_t stream_index);

/* HTS_ModelSet_use_gv: get GV flag */
HTS_Boolean HTS_ModelSet_use_gv(HTS_ModelSet * ms, size_t stream_index);

/* HTS_ModelSet_get_duration_index: get index of duration tree and PDF */
void HTS_ModelSet_get_duration_index(HTS_ModelSet * ms, size_t voice_index, const char *string, size_t * tree_index, size_t * pdf_index);

/* HTS_ModelSet_get_duration: get duration using interpolation weight */
void HTS_ModelSet_get_duration(HTS_ModelSet * ms, const char *string, const double *iw, double *mean, double *vari);

/* HTS_ModelSet_get_parameter_index: get index of parameter tree and PDF */
void HTS_ModelSet_get_parameter_index(HTS_ModelSet * ms, size_t voice_index, size_t stream_index, size_t state_index, const char *string, size_t * tree_index, size_t * pdf_index);

/* HTS_ModelSet_get_parameter: get parameter using interpolation weight */
void HTS_ModelSet_get_parameter(HTS_ModelSet * ms, size_t stream_index, size_t state_index, const char *string, const double *iw, double *mean, double *vari, double *msd);

void HTS_ModelSet_get_gv_index(HTS_ModelSet * ms, size_t voice_index, size_t stream_index, const char *string, size_t * tree_index, size_t * pdf_index);

/* HTS_ModelSet_get_gv: get GV using interpolation weight */
void HTS_ModelSet_get_gv(HTS_ModelSet * ms, size_t stream_index, const char *string, const double *iw, double *mean, double *vari);

/* HTS_ModelSet_clear: free model set */
void HTS_ModelSet_clear(HTS_ModelSet * ms);

/* label ----------------------------------------------------------- */

/* HTS_Label_initialize: initialize label */
void HTS_Label_initialize(HTS_Label * label);

/* HTS_Label_load_from_fn: load label from file name */
void HTS_Label_load_from_fn(HTS_Label * label, size_t sampling_rate, size_t fperiod, const char *fn);

/* HTS_Label_load_from_strings: load label list from string list */
void HTS_Label_load_from_strings(HTS_Label * label, size_t sampling_rate, size_t fperiod, char **lines, size_t num_lines);

/* HTS_Label_get_size: get number of label string */
size_t HTS_Label_get_size(HTS_Label * label);

/* HTS_Label_get_string: get label string */
const char *HTS_Label_get_string(HTS_Label * label, size_t index);

/* HTS_Label_get_start_frame: get start frame */
double HTS_Label_get_start_frame(HTS_Label * label, size_t index);

/* HTS_Label_get_end_frame: get end frame */
double HTS_Label_get_end_frame(HTS_Label * label, size_t index);

/* HTS_Label_clear: free label */
void HTS_Label_clear(HTS_Label * label);

/* sstream --------------------------------------------------------- */

/* HTS_SStreamSet_initialize: initialize state stream set */
void HTS_SStreamSet_initialize(HTS_SStreamSet * sss);

/* HTS_SStreamSet_create: parse label and determine state duration */
HTS_Boolean HTS_SStreamSet_create(HTS_SStreamSet * sss, HTS_ModelSet * ms, HTS_Label * label, HTS_Boolean phoneme_alignment_flag, double speed, double *duration_iw, double **parameter_iw, double **gv_iw);

/* HTS_SStreamSet_get_nstream: get number of stream */
size_t HTS_SStreamSet_get_nstream(HTS_SStreamSet * sss);

/* HTS_SStreamSet_get_vector_length: get vector length */
size_t HTS_SStreamSet_get_vector_length(HTS_SStreamSet * sss, size_t stream_index);

/* HTS_SStreamSet_is_msd: get MSD flag */
HTS_Boolean HTS_SStreamSet_is_msd(HTS_SStreamSet * sss, size_t stream_index);

/* HTS_SStreamSet_get_total_state: get total number of state */
size_t HTS_SStreamSet_get_total_state(HTS_SStreamSet * sss);

/* HTS_SStreamSet_get_total_frame: get total number of frame */
size_t HTS_SStreamSet_get_total_frame(HTS_SStreamSet * sss);

/* HTS_SStreamSet_get_msd: get msd parameter */
double HTS_SStreamSet_get_msd(HTS_SStreamSet * sss, size_t stream_index, size_t state_index);

/* HTS_SStreamSet_window_size: get dynamic window size */
size_t HTS_SStreamSet_get_window_size(HTS_SStreamSet * sss, size_t stream_index);

/* HTS_SStreamSet_get_window_left_width: get left width of dynamic window */
int HTS_SStreamSet_get_window_left_width(HTS_SStreamSet * sss, size_t stream_index, size_t window_index);

/* HTS_SStreamSet_get_window_right_width: get right width of dynamic window */
int HTS_SStreamSet_get_window_right_width(HTS_SStreamSet * sss, size_t stream_index, size_t window_index);

/* HTS_SStreamSet_get_window_coefficient: get coefficient of dynamic window */
double HTS_SStreamSet_get_window_coefficient(HTS_SStreamSet * sss, size_t stream_index, size_t window_index, int coefficient_index);

/* HTS_SStreamSet_get_window_max_width: get max width of dynamic window */
size_t HTS_SStreamSet_get_window_max_width(HTS_SStreamSet * sss, size_t stream_index);

/* HTS_SStreamSet_use_gv: get GV flag */
HTS_Boolean HTS_SStreamSet_use_gv(HTS_SStreamSet * sss, size_t stream_index);

/* HTS_SStreamSet_get_duration: get state duration */
size_t HTS_SStreamSet_get_duration(HTS_SStreamSet * sss, size_t state_index);

/* HTS_SStreamSet_get_mean: get mean parameter */
double HTS_SStreamSet_get_mean(HTS_SStreamSet * sss, size_t stream_index, size_t state_index, size_t vector_index);

/* HTS_SStreamSet_set_mean: set mean parameter */
void HTS_SStreamSet_set_mean(HTS_SStreamSet * sss, size_t stream_index, size_t state_index, size_t vector_index, double f);

/* HTS_SStreamSet_get_vari: get variance parameter */
double HTS_SStreamSet_get_vari(HTS_SStreamSet * sss, size_t stream_index, size_t state_index, size_t vector_index);

/* HTS_SStreamSet_set_vari: set variance parameter */
void HTS_SStreamSet_set_vari(HTS_SStreamSet * sss, size_t stream_index, size_t state_index, size_t vector_index, double f);

/* HTS_SStreamSet_get_gv_mean: get GV mean parameter */
double HTS_SStreamSet_get_gv_mean(HTS_SStreamSet * sss, size_t stream_index, size_t vector_index);

/* HTS_SStreamSet_get_gv_mean: get GV variance parameter */
double HTS_SStreamSet_get_gv_vari(HTS_SStreamSet * sss, size_t stream_index, size_t vector_index);

/* HTS_SStreamSet_set_gv_switch: set GV switch */
void HTS_SStreamSet_set_gv_switch(HTS_SStreamSet * sss, size_t stream_index, size_t state_index, HTS_Boolean i);

/* HTS_SStreamSet_get_gv_switch: get GV switch */
HTS_Boolean HTS_SStreamSet_get_gv_switch(HTS_SStreamSet * sss, size_t stream_index, size_t state_index);

/* HTS_SStreamSet_clear: free state stream set */
void HTS_SStreamSet_clear(HTS_SStreamSet * sss);

/* HTS_PStreamSet_initialize: initialize parameter stream set */
void HTS_PStreamSet_initialize(HTS_PStreamSet * pss);

/* HTS_PStreamSet_create: parameter generation using GV weight */
HTS_Boolean HTS_PStreamSet_create(HTS_PStreamSet * pss, HTS_SStreamSet * sss, double *msd_threshold, double *gv_weight);

/* HTS_PStreamSet_get_nstream: get number of stream */
size_t HTS_PStreamSet_get_nstream(HTS_PStreamSet * pss);

/* HTS_PStreamSet_get_static_length: get features length */
size_t HTS_PStreamSet_get_vector_length(HTS_PStreamSet * pss, size_t stream_index);

/* HTS_PStreamSet_get_total_frame: get total number of frame */
size_t HTS_PStreamSet_get_total_frame(HTS_PStreamSet * pss);

/* HTS_PStreamSet_get_parameter: get parameter */
double HTS_PStreamSet_get_parameter(HTS_PStreamSet * pss, size_t stream_index, size_t frame_index, size_t vector_index);

/* HTS_PStreamSet_get_parameter_vector: get parameter vector */
double *HTS_PStreamSet_get_parameter_vector(HTS_PStreamSet * pss, size_t stream_index, size_t frame_index);

/* HTS_PStreamSet_get_msd_flag: get generated MSD flag per frame */
HTS_Boolean HTS_PStreamSet_get_msd_flag(HTS_PStreamSet * pss, size_t stream_index, size_t frame_index);

/* HTS_PStreamSet_is_msd: get MSD flag */
HTS_Boolean HTS_PStreamSet_is_msd(HTS_PStreamSet * pss, size_t stream_index);

/* HTS_PStreamSet_clear: free parameter stream set */
void HTS_PStreamSet_clear(HTS_PStreamSet * pss);

/* gstream --------------------------------------------------------- */

/* HTS_GStreamSet_initialize: initialize generated parameter stream set */
void HTS_GStreamSet_initialize(HTS_GStreamSet * gss);

/* HTS_GStreamSet_create: generate speech */
HTS_Boolean HTS_GStreamSet_create(HTS_GStreamSet * gss, HTS_PStreamSet * pss, size_t stage, HTS_Boolean use_log_gain, size_t sampling_rate, size_t fperiod, double alpha, double beta, HTS_Boolean * stop, double volume, HTS_Audio * audio);

/* HTS_GStreamSet_create: generate speech with given lf0 */
HTS_Boolean HTS_GStreamSet_create_me_with_lf0(HTS_GStreamSet * gss, HTS_PStreamSet * pss, size_t stage, HTS_Boolean use_log_gain, size_t sampling_rate, size_t fperiod, double alpha, double beta, HTS_Boolean * stop, double volume, HTS_Audio * audio, size_t me_num_filters, size_t me_filter_order, const double ** me_filter, size_t pd_filter_order, const double * pd_filter, double * xp_sig, double * xn_sig, double * hp, double * hn, const double * ilf0, size_t ilf0_nframes);

/* HTS_GStreamSet_get_total_nsamples: get total number of sample */
size_t HTS_GStreamSet_get_total_nsamples(HTS_GStreamSet * gss);

/* HTS_GStreamSet_get_total_frame: get total number of frame */
size_t HTS_GStreamSet_get_total_frame(HTS_GStreamSet * gss);

/* HTS_GStreamSet_get_static_length: get features length */
size_t HTS_GStreamSet_get_vector_length(HTS_GStreamSet * gss, size_t stream_index);

/* HTS_GStreamSet_get_speech: get synthesized speech parameter */
double HTS_GStreamSet_get_speech(HTS_GStreamSet * gss, size_t sample_index);

/* HTS_GStreamSet_get_parameter: get generated parameter */
double HTS_GStreamSet_get_parameter(HTS_GStreamSet * gss, size_t stream_index, size_t frame_index, size_t vector_index);

/* HTS_GStreamSet_clear: free generated parameter stream set */
void HTS_GStreamSet_clear(HTS_GStreamSet * gss);

/* HTS_Vocoder: structure for setting of vocoder */
typedef struct _HTS_Vocoder {
   HTS_Boolean is_first;
   size_t stage;                /* Gamma=-1/stage: if stage=0 then Gamma=0 */
   double gamma;                /* Gamma */
   HTS_Boolean use_log_gain;    /* log gain flag (for LSP) */
   size_t fprd;                 /* frame shift */
   unsigned long next;          /* temporary variable for random generator */
   HTS_Boolean gauss;           /* flag to use Gaussian noise */
   double rate;                 /* sampling rate */
   double pitch_of_curr_point;  /* used in excitation generation */
   double pitch_counter;        /* used in excitation generation */
   double pitch_inc_per_point;  /* used in excitation generation */
   double *excite_ring_buff;    /* used in excitation generation */
   size_t excite_buff_size;     /* used in excitation generation */
   size_t excite_buff_index;    /* used in excitation generation */
   unsigned char sw;            /* switch used in random generator */
   int x;                       /* excitation signal */
   double *freqt_buff;          /* used in freqt */
   size_t freqt_size;           /* buffer size for freqt */
   double *spectrum2en_buff;    /* used in spectrum2en */
   size_t spectrum2en_size;     /* buffer size for spectrum2en */
   double r1, r2, s;            /* used in random generator */
   double *postfilter_buff;     /* used in postfiltering */
   size_t postfilter_size;      /* buffer size for postfiltering */
   double *c, *cc, *cinc, *d1;  /* used in the MLSA/MGLSA filter */
   double *lsp2lpc_buff;        /* used in lsp2lpc */
   size_t lsp2lpc_size;         /* buffer size of lsp2lpc */
   double *gc2gc_buff;          /* used in gc2gc */
   size_t gc2gc_size;           /* buffer size for gc2gc */
} HTS_Vocoder;

/* HTS_Vocoder_initialize: initialize vocoder */
void HTS_Vocoder_initialize(HTS_Vocoder * v, size_t m, size_t stage, HTS_Boolean use_log_gain, size_t rate, size_t fperiod);

/* HTS_Vocoder_synthesize: pulse/noise excitation and MLSA/MGLSA filster based waveform synthesis */
void HTS_Vocoder_synthesize(HTS_Vocoder * v, size_t m, double lf0, double *spectrum, size_t nlpf, double *lpf, double alpha, double beta, double volume, double *rawdata, HTS_Audio * audio);

/* HTS_Vocoder_clear: clear vocoder */
void HTS_Vocoder_clear(HTS_Vocoder * v);

/* HTS_Vocoder_ME: structure for setting of vocoder (mixed excitation) */
typedef struct _HTS_Vocoder_ME {
   HTS_Vocoder *v;                /* hts engine vocoder structure */
   
   /* mixed excitation */
   double  *xp_sig;         /* pulse signal, the size of this should be the filter order */
   double  *xn_sig;         /* noise signal, the size of this should be the filter order */
   double  *hp;             /* pulse shaping filter, size of the filter order            */
   double  *hn;             /* noise shaping filter, size of the filter order            */
   size_t  num_filters;     /* number of filters                                         */
   size_t  filter_order;    /* filter order                                              */
   const double **h;        /* me filter coefficients                                    */
} HTS_Vocoder_ME;

/* HTS_Vocoder_initialize_me: initialize vocoder (mixed excitation) */
void HTS_Vocoder_initialize_me(HTS_Vocoder_ME * v_me, size_t m, size_t stage, HTS_Boolean use_log_gain, size_t rate, size_t fperiod,
			       size_t num_filters, size_t filter_order, const double **me_filter,
			       double *xp_sig, double *xn_sig, double *hp, double *hn);

/* HTS_Vocoder_synthesize_me: mixed excitation and MLSA/MGLSA filster based waveform synthesis */
void HTS_Vocoder_synthesize_me(HTS_Vocoder_ME * v_me, size_t m, double lf0,
			       double *spectrum, double *strengths, double alpha,
			       double beta, double volume, double *rawdata, HTS_Audio * audio);

/* HTS_Vocoder_clear_me: clear vocoder (mixed excitation) */
void HTS_Vocoder_clear_me(HTS_Vocoder_ME * v_me);
