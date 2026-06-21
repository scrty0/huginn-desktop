using System.Threading.Tasks;
namespace Huginn.Core.Services {
    public interface IMlInferenceService { Task<float> GetSpoofScoreAsync(float[] audioData); }
}
